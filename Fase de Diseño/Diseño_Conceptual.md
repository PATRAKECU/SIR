# Diseño Conceptual

## 1. Propósito del sistema
El objetivo central de este sistema es proporcinar al usuario una aplicación intuitiva
y de fácil uso para realizar análisis de pronóstico de propagación de enfermedades usando
el modelo SIR (Susceptibles, Infectados, Recuperados). 

## 2. Usuarios objetivo
- Estudiantes universitarios
- Docentes
- Investigadores
- Usuarios no expertos

## 3. Necesidades del usuario
Los usuarios de esta aplicación buscan claridad de uso, visualización adecuada de componentes dentro de cada módulo,
rapidez de la plataforma para ejecutar, visualizar y generar reportes de análisis,
y por último, simplicidad para evitar la saturaci;on visual y cognitiva.

## 4. Contexto de uso
Los usuarios harán uso de esta aplicación en aulas de clase, laboratorios y seminarios o cursos sobre epidemiología.
Cada usuario podrá acceder a la aplicación desde su ordenador o dispositivo móvil con acceso a internet ya que
es una aplicación adaptable (responsive).

## 5. Tareas principales del usuario
- Crear cuenta
- Autenticarse en su cuenta
- Ingresar parámetros
- Ejecutar simulación
- Revisar resultados
- Generar reporte

## 6. Criterios de diseño (HCI)

### Usabilidad (Nielsen)
Siguiendo los principios de usabilidad de Nielsen (Nielsen, 1994), el simulador incorpora:

**Visibilidad del estado del sistema**

El usuario recibe retroalimentación inmediata al ejecutar una simulación o editar parámetros.

**Correspondencia entre el sistema y el mundo real:**

Los términos utilizados (población, tasa de contagio, días, etc.) corresponden al lenguaje epidemiológico estándar.

**Control y libertad del usuario:**

El usuario puede editar, repetir o eliminar simulaciones sin riesgo de perder información accidentalmente.

**Consistencia y estándares:**

Se emplean patrones visuales y de interacción comunes (formularios, botones, navegación superior).

**Prevención de errores:**

Los formularios validan rangos numéricos y tipos de datos antes de ejecutar el modelo.

Adicionalmente, se realiza suavización y restricción de datos para evitar errores de renderización en gráficos con Plotly y Matplotlib.

### Carga cognitiva reducida (Sweller)

La teoría de carga cognitiva (Sweller, 1988) indica que las interfaces deben minimizar el esfuerzo mental innecesario.

**En el simulador:**

•	Los gráficos interactivos permiten explorar valores sin saturar al usuario con tablas extensas.

•	El uso de colores diferenciados para S, I y R facilita la interpretación inmediata de tendencias.

•	La interfaz evita elementos distractores y mantiene un diseño limpio y académico.

Además, la visualización de datos sigue principios de Tufte (1990), privilegiando claridad, precisión y eficiencia gráfica.
### Accesibilidad (WCAG)
Siguiendo las pautas WCAG (W3C, 2025), el simulador incorpora:

•	Contrastes adecuados entre texto y fondo.

•	Navegación clara en dispositivos móviles.

•	Botones con estados hover visibles y consistentes.

•	Estructura semántica en HTML para mejorar la comprensión.

Esto garantiza que el simulador sea accesible para un rango amplio de usuarios.

## 7. Justificación del enfoque centrado en el usuario
Este enfoque permite analizar la creación de un sistema desde el punto de vista del usuario.
Mediante este análisis se puede determinar las necesidades específicas del usuario para mejorar
al máximo la experiencia general del usuario (UX).