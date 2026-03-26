from flask_wtf import FlaskForm
from wtforms import (
    FloatField,
    SubmitField,
    StringField,
    PasswordField,
    IntegerField
)
from wtforms.validators import DataRequired, NumberRange, EqualTo, Length, Email

# Form for entering SIR analysis parameters
class SIRForm(FlaskForm):
    population = IntegerField(
        "Población inicial",
        default=1000,
        validators=[
            DataRequired(),
            NumberRange(min=1, max=10_000_000_000,
                        message="La población debe estar entre 1 y 10 mil millones.")
        ]
    )

    beta = FloatField(
        "Tasa de contagio (β)",
        default=0.3,
        validators=[
            DataRequired(),
            NumberRange(min=0, max=1,
                        message="β debe estar entre 0 y 1.")
        ]
    )

    gamma = FloatField(
        "Tasa de recuperación (γ)",
        default=0.1,
        validators=[
            DataRequired(),
            NumberRange(min=0, max=1,
                        message="γ debe estar entre 0 y 1.")
        ]
    )

    days = IntegerField(
        "Días de simulación",
        default=160,
        validators=[
            DataRequired(),
            NumberRange(min=1, max=3650,
                        message="Los días deben estar entre 1 y 3650.")
        ]
    )

    submit = SubmitField("Generar análisis")

    # --- Validaciones científicas suaves ---
    def validate(self, extra_validators=None):
        valid = super().validate(extra_validators)

        # Crear lista de advertencias
        self.warnings = []

        beta = self.beta.data
        gamma = self.gamma.data

        # γ = 0 → físicamente imposible
        if gamma == 0:
            self.gamma.errors.append("γ no puede ser cero: impediría la recuperación.")
            return False

        # Cálculo de R0
        R0 = beta / gamma if gamma > 0 else None

        # Advertencias científicas
        if R0 is not None:
            if R0 < 1:
                self.warnings.append(
                    f"R₀ = {R0:.2f}. El brote no crecerá (R₀ < 1)."
                )
            elif R0 > 3:
                self.warnings.append(
                    f"R₀ = {R0:.2f}. Epidemia altamente contagiosa (R₀ > 3)."
                )

        # β ≈ γ → equilibrio rápido
        if abs(beta - gamma) < 0.01:
            self.warnings.append(
                "β y γ son muy similares: la infección tenderá al equilibrio rápidamente."
            )

        return valid


# Form for editing SIR analyses
class EditAnalysisForm(FlaskForm):
    population = IntegerField("Población inicial", validators=[DataRequired(), NumberRange(min=1)])
    beta = FloatField("Tasa de contagio (β)", validators=[DataRequired(), NumberRange(min=0)])
    gamma = FloatField("Tasa de recuperación (γ)", validators=[DataRequired(), NumberRange(min=0)])
    days = IntegerField("Días de simulación", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Actualizar análisis")


# Form for user registration
class RegisterForm(FlaskForm):
    name = StringField(
        "Nombre completo",
        validators=[DataRequired(), Length(min=3)]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Ingrese un email válido.")]
    )
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(), Length(min=6)]
    )
    confirmation = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(),
            EqualTo("password", message="Las contraseñas deben coincidir.")
        ]
    )
    submit = SubmitField("Registrarse")


# Form for user login
class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Ingrese un email válido.")]
    )
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(), Length(min=6)]
    )
    submit = SubmitField("Iniciar sesión")



# Form for changing the user's password
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Current Password",
        validators=[DataRequired()]
    )
    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=6),
            EqualTo("confirm_password", message="Passwords must match.")
        ]
    )
    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[DataRequired()]
    )
    submit = SubmitField("Change Password")

