# Simulador Epidemiológico – Modelo SIR
#### Video Demo: *(pendiente de enlace si aplica)*  
#### Descripción

El **Simulador Epidemiológico SIR** es una aplicación web científica que permite modelar la propagación de enfermedades infecciosas mediante el modelo clásico **SIR (Susceptible – Infectado – Recuperado)**.  
Diseñado para estudiantes, docentes e investigadores, el sistema permite ingresar parámetros epidemiológicos, visualizar la evolución temporal de la enfermedad y generar reportes en PDF con gráficos estáticos.

El proyecto fue desarrollado con **Flask (Python)**, **SQLite**, **Matplotlib**, **Plotly** y **Bootstrap 5**.  
Se implementó autenticación segura, validación dinámica de formularios y un diseño completamente adaptable.  
La tecnología Copilot fue utilizada como apoyo para decisiones técnicas y búsqueda de bibliografía.

---

## Fundamento Matemático

El modelo SIR describe la dinámica de transmisión de una enfermedad mediante el siguiente sistema de ecuaciones diferenciales:

```text
dS/dt = -βSI
dI/dt = βSI - γI
dR/dt = γI
```
Donde:

- S(t): población susceptible
- I(t): población infectada
- R(t): población recuperada
- β: tasa de contagio
- γ: tasa de recuperación


El sistema se resuelve numéricamente para obtener las curvas epidemiológicas que representan la evolución de la enfermedad en el tiempo.

---

## Características

- 📊 **Gráfico Interactivo**: Curvas S, I y R generadas con Plotly, con valores accesibles mediante hover.
- 🖼️ **Gráfico Estático para PDF**: Generación de imágenes PNG con Matplotlib.
- 📄 **Exportación a PDF**: Reportes formateados con WeasyPrint.
- 🔐 **Autenticación de Usuarios**: Registro, inicio de sesión y cierre de sesión seguro.
- 📁 **Historial de Análisis**: Cada usuario puede consultar, editar y eliminar sus simulaciones.
- 🌐 **Diseño Responsive**: Interfaz optimizada para dispositivos móviles y escritorio.
- 🧮 **Modelo Numérico**: Implementación robusta del sistema SIR con integración temporal.
- 🧪 **Pruebas Unitarias e Integración**: Cobertura de rutas, modelo matemático y CRUD.

---

## Estructura del Proyecto

- `__init__.py`: Inicializa la aplicación Flask y configura la base de datos.
- `run.py`: Punto de entrada para ejecutar la aplicación localmente.
- `routes.py`: Contiene todas las rutas, lógica del modelo SIR, autenticación y exportación a PDF.
- `forms.py`: Formularios WTForms para ingreso de parámetros, login y registro.
- `plot.py`: Funciones para generar gráficos interactivos y estáticos.
- `templates/`: Plantillas HTML con Jinja2, incluyendo:
  - `index.html`
  - `create_analysis.html`
  - `analysis_detail.html`
  - `edit_analysis.html`
  - `history.html`
  - `report_pdf.html`
  - `report_preview.html`
  - `login.html`
  - `register.html`
  - `layout.html`
- `static/css/theme_sir.css`: Tema visual personalizado.
- `static/css/pdf_style.css`: Estilos solemnes para reportes PDF.
- `static/static_plots/`: Carpeta donde se guardan los gráficos PNG.
- `schema.sql`: Script para crear las tablas principales.
- `requirements.txt`: Dependencias necesarias para ejecutar la aplicación.
- `tests/`: Pruebas unitarias y de integración con pytest.

---

## Decisiones de Diseño

- **Plotly para Interactividad**: Permite explorar valores puntuales de S, I y R.
- **Matplotlib para PDF**: Compatible con WeasyPrint y adecuado para reportes estáticos.
- **WeasyPrint para Exportación**: Genera documentos PDF de alta calidad a partir de HTML y CSS.
- **Control de Acceso por Sesión**: Cada análisis está asociado a un `user_id`.
- **Validación de Formularios**: WTForms asegura integridad de datos.
- **Rutas Protegidas**: Decorador `@login_required` para evitar accesos no autorizados.
- **Pruebas Automatizadas**: Validan el CRUD, el modelo SIR y las rutas principales.

---

## Retos y Soluciones

- **Generación de PDF en Windows**: Se resolvió instalando GTK3 y reinstalando WeasyPrint.
- **Rutas Relativas en PDF**: Se implementó `base_url` para cargar imágenes y CSS correctamente.
- **Responsividad del Navbar**: Se añadió toggler y estilos personalizados.
- **Contraste de Botones**: Ajustes CSS para mejorar accesibilidad visual.
- **Pruebas con Sesión**: Uso de `client.session_transaction()` para simular usuarios autenticados.
- **Modelo SIR**: Se implementó integración numérica estable y eficiente.

---

## Cómo Ejecutar

1. Clonar el repositorio.  
2. Crear un entorno virtual e instalar dependencias:
    pip install -r requirements.txt
3. Crear la base de datos ejecutando el script SQL:
    sqlite3 sir.db < schema.sql
4. Ejecutar la aplicación:
    python run.py
5. Acceder en el navegador:
    http://localhost:5000

---

## Cómo Ejecutar las Pruebas

1. Instalar dependencias de desarrollo:
    pip install pytest pytest-flask
2. Ejecutar:
    pytest

---

## Licencia

Este proyecto fue desarrollado por Patricio Agurto con fines académicos como parte del caso de estudio de la materia: Human-Computer Interaction, and Digital Citizenship parte de la Maestría en Ingeniería de Software y Sistemas Informáticos de Broward International University.
