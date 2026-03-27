from flask import render_template, request, redirect, url_for, session, Response, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from app.forms import SIRForm, RegisterForm, LoginForm, EditAnalysisForm
import math
import sqlite3
from app.plot import generate_sir_plot_html, generate_sir_plot_image
from functools import wraps
import logging
from weasyprint import HTML
from datetime import datetime
import os
import numpy as np


# Debug configuration for user information
logging.basicConfig(level=logging.DEBUG)

# Connect to database in SQLite3
def get_db_connection():
    conn = sqlite3.connect("sir.db")
    # Enable dictionary-style access to columns
    conn.row_factory = sqlite3.Row
    return conn

# Establish function to require uses to login to access certain services
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# Prevent caching of sensitive data in shared or public browsers
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = "0"
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        session.clear()

        email = form.email.data
        password = form.password.data

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()
        conn.close()

        if user is None or not check_password_hash(user["password"], password):
            form.email.errors.append("Email o contraseña incorrectos.")
            return render_template("login.html", form=form)

        session["user_id"] = user["id"]
        session["name"] = user["name"]

        return redirect(url_for("index"))

    return render_template("login.html", form=form)



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password)

        try:
            conn = get_db_connection()
            conn.execute("""
                INSERT INTO users (name, email, password)
                VALUES (?, ?, ?)
            """, (name, email, hashed_password))
            conn.commit()
            conn.close()
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            form.email.errors.append("Este email ya está registrado.")

    return render_template("register.html", form=form)
    

@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/analysis", methods=["GET", "POST"])
@login_required
def create_analysis():
    form = SIRForm()

    if form.validate_on_submit():
        population = form.population.data
        beta = form.beta.data
        gamma = form.gamma.data
        days = form.days.data

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO analysis (user_id, population, beta, gamma, days, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (session["user_id"], population, beta, gamma, days, datetime.now()))
        conn.commit()

        analysis_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.close()

        return redirect(url_for("analysis_detail", analysis_id=analysis_id))

    return render_template("create_analysis.html", form=form)


@app.route("/history")
@login_required
def history():
    conn = get_db_connection()
    rows = conn.execute("""
        SELECT *
        FROM analysis
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (session["user_id"],)).fetchall()
    conn.close()

    return render_template("history.html", rows=rows)


@app.route("/analysis/<int:analysis_id>")
@login_required
def analysis_detail(analysis_id):
    # Obtener análisis desde la base de datos
    conn = get_db_connection()
    analysis = conn.execute("""
        SELECT *
        FROM analysis
        WHERE id = ? AND user_id = ?
    """, (analysis_id, session["user_id"])).fetchone()
    conn.close()

    # Si no existe o no pertenece al usuario, redirigir
    if analysis is None:
        return redirect(url_for("analysis"))

    # Generar gráfico dinámico con Plotly
    plot_html, S, I, R = generate_sir_plot_html(
        population=analysis["population"],
        beta=analysis["beta"],
        gamma=analysis["gamma"],
        days=analysis["days"]
    )

    # Cálculo de métricas epidemiológicas
    R0 = analysis["beta"] / analysis["gamma"]
    peak_day = int(np.argmax(I))
    peak_value = float(max(I))
    final_recovered_pct = (R[-1] / analysis["population"]) * 100

    # Duración aproximada del brote (I cae por debajo de 1)
    threshold = 1
    duration = next((i for i, val in enumerate(I[::-1]) if val > threshold), 0)
    duration = len(I) - duration

    return render_template(
        "analysis_detail.html",
        analysis=analysis,
        plot_html=plot_html,
        R0=R0,
        peak_day=peak_day,
        peak_value=peak_value,
        duration=duration,
        final_recovered_pct=final_recovered_pct
    )


@app.route("/analysis/<int:analysis_id>/edit", methods=["GET", "POST"])
@login_required
def edit_analysis(analysis_id):
    form = EditAnalysisForm()

    # Obtener análisis desde la base de datos
    conn = get_db_connection()
    analysis = conn.execute("""
        SELECT *
        FROM analysis
        WHERE id = ? AND user_id = ?
    """, (analysis_id, session["user_id"])).fetchone()

    # Si no existe o no pertenece al usuario
    if analysis is None:
        conn.close()
        return redirect(url_for("history"))

    # Prellenar formulario con datos actuales
    if request.method == "GET":
        form.population.data = analysis["population"]
        form.beta.data = analysis["beta"]
        form.gamma.data = analysis["gamma"]
        form.days.data = analysis["days"]

    # Procesar actualización
    if form.validate_on_submit():
        population = form.population.data
        beta = form.beta.data
        gamma = form.gamma.data
        days = form.days.data

        conn.execute("""
            UPDATE analysis
            SET population = ?, beta = ?, gamma = ?, days = ?, created_at = ?
            WHERE id = ? AND user_id = ?
        """, (population, beta, gamma, days, datetime.now(), analysis_id, session["user_id"]))

        conn.commit()
        conn.close()

        return redirect(url_for("analysis_detail", analysis_id=analysis_id))

    conn.close()
    return render_template("edit_analysis.html", form=form, analysis_id=analysis_id)


@app.route("/analysis/<int:analysis_id>/delete")
@login_required
def delete_analysis(analysis_id):
    conn = get_db_connection()
    conn.execute("""
        DELETE FROM analysis
        WHERE id = ? AND user_id = ?
    """, (analysis_id, session["user_id"]))
    conn.commit()
    conn.close()

    return redirect(url_for("history"))


@app.route("/report/<int:analysis_id>")
@login_required
def report_preview(analysis_id):
    # Obtener análisis desde la base de datos
    conn = get_db_connection()
    analysis = conn.execute("""
        SELECT *
        FROM analysis
        WHERE id = ? AND user_id = ?
    """, (analysis_id, session["user_id"])).fetchone()
    conn.close()

    # Si no existe o no pertenece al usuario
    if analysis is None:
        return redirect(url_for("history"))

    # Generar gráfico estático para vista previa
    absolute_path, relative_path, S, I, R = generate_sir_plot_image(
        population=analysis["population"],
        beta=analysis["beta"],
        gamma=analysis["gamma"],
        days=analysis["days"]
    )

    # ================================
    # Cálculo de métricas epidemiológicas
    # ================================

    R0 = analysis["beta"] / analysis["gamma"]
    peak_day = int(np.argmax(I))
    peak_value = float(max(I))
    final_recovered_pct = (R[-1] / analysis["population"]) * 100

    # Duración aproximada del brote (I cae por debajo de 1)
    threshold = 1
    duration = next((i for i, val in enumerate(I[::-1]) if val > threshold), 0)
    duration = len(I) - duration

    return render_template(
        "report_preview.html",
        analysis=analysis,
        plot_path=relative_path,
        R0=R0,
        peak_day=peak_day,
        peak_value=peak_value,
        duration=duration,
        final_recovered_pct=final_recovered_pct
    )


@app.route("/report/<int:analysis_id>/pdf")
@login_required
def report_pdf(analysis_id):
    # Obtener análisis desde la base de datos
    conn = get_db_connection()
    analysis = conn.execute("""
        SELECT *
        FROM analysis
        WHERE id = ? AND user_id = ?
    """, (analysis_id, session["user_id"])).fetchone()
    conn.close()

    # Si no existe o no pertenece al usuario
    if analysis is None:
        return redirect(url_for("history"))

    # Generar gráfico estático con Matplotlib
    absolute_path, relative_path, S, I, R = generate_sir_plot_image(
        population=analysis["population"],
        beta=analysis["beta"],
        gamma=analysis["gamma"],
        days=analysis["days"]
    )

    # Verificar que el archivo existe
    assert os.path.exists(absolute_path)
    assert os.access(absolute_path, os.R_OK)

    # Preparar rutas para WeasyPrint
    project_root = current_app.root_path
    rel_path = os.path.relpath(absolute_path, start=project_root).replace(os.path.sep, '/')
    base_url = f'file:///{project_root.replace(os.path.sep, "/")}/'

    # ================================
    # Cálculo de métricas epidemiológicas
    # ================================
    R0 = analysis["beta"] / analysis["gamma"]
    peak_day = int(np.argmax(I))
    peak_value = float(max(I))
    final_recovered_pct = (R[-1] / analysis["population"]) * 100

    threshold = 1
    duration = next((i for i, val in enumerate(I[::-1]) if val > threshold), 0)
    duration = len(I) - duration

    # Renderizar HTML del reporte
    html = render_template(
        "report_pdf.html",
        analysis=analysis,
        plot_path=rel_path,
        base_url=base_url,
        R0=R0,
        peak_day=peak_day,
        peak_value=peak_value,
        duration=duration,
        final_recovered_pct=final_recovered_pct
    )

    # Generar PDF
    pdf = HTML(string=html, base_url=base_url).write_pdf()

    # Enviar PDF al navegador
    return Response(pdf, mimetype="application/pdf", headers={
        "Content-Disposition": f"inline; filename=analysis_{analysis_id}.pdf"
    })
