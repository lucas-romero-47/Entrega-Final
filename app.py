"""
NutriIA - Asistente de Alimentación Personalizada con IA
Proyecto Final - Prompt Engineering para Programadores | CoderHouse
Autor: Lucas Romero | Comisión: #86240
"""

import streamlit as st
from openai import OpenAI

# ─── Configuración de página ────────────────────────────────────────────────
st.set_page_config(
    page_title="NutriIA",
    page_icon="🥗",
    layout="centered"
)

# ─── Estilos ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .main-header h1 { font-size: 2.5rem; margin: 0; }
    .main-header p  { font-size: 1.1rem; margin: 0.5rem 0 0; opacity: 0.9; }
    .info-card {
        background: #f8f9fa;
        border-left: 4px solid #2ecc71;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .footer {
        text-align: center;
        color: #888;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🥗 NutriIA</h1>
    <p>Tu nutricionista virtual · Planes de alimentación personalizados con IA</p>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar: API Key ────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuración")
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    st.markdown("---")
    st.markdown("**NutriIA** genera planes de comidas semanales personalizados usando GPT-4.")
    st.markdown("*Comisión #86240 · Lucas Romero*")

# ─── Formulario de perfil ────────────────────────────────────────────────────
st.subheader("📋 Tu perfil nutricional")

col1, col2, col3 = st.columns(3)
with col1:
    edad = st.number_input("Edad", min_value=10, max_value=100, value=30, step=1)
with col2:
    peso = st.number_input("Peso (kg)", min_value=30.0, max_value=250.0, value=70.0, step=0.5)
with col3:
    altura = st.number_input("Altura (cm)", min_value=100, max_value=250, value=170, step=1)

col4, col5 = st.columns(2)
with col4:
    objetivo = st.selectbox("Objetivo", ["Bajar peso", "Ganar músculo", "Mantener peso", "Mejorar salud general"])
with col5:
    sexo = st.selectbox("Sexo biológico", ["Masculino", "Femenino"])

restricciones = st.multiselect(
    "Restricciones alimentarias",
    ["Vegetariano", "Vegano", "Sin gluten", "Sin lactosa", "Sin mariscos", "Sin frutos secos", "Ninguna"],
    default=["Ninguna"]
)
restricciones_str = ", ".join(restricciones) if restricciones else "Ninguna"

actividad = st.select_slider(
    "Nivel de actividad física",
    options=["Sedentario", "Ligero (1-2 días/semana)", "Moderado (3-4 días/semana)", "Activo (5+ días/semana)"]
)

# ─── Botón de acción ─────────────────────────────────────────────────────────
st.markdown("---")
generar = st.button("🚀 Generar mi plan semanal", use_container_width=True, type="primary")

# ─── Lógica de generación ────────────────────────────────────────────────────
if generar:
    if not api_key:
        st.error("⚠️ Ingresá tu OpenAI API Key en el panel lateral para continuar.")
    else:
        # Construcción del prompt estructurado
        prompt = f"""Eres un nutricionista experto en alimentación saludable y balanceada.

El usuario tiene el siguiente perfil:
- Edad: {edad} años
- Sexo: {sexo}
- Peso: {peso} kg
- Altura: {altura} cm
- Objetivo: {objetivo}
- Restricciones alimentarias: {restricciones_str}
- Nivel de actividad física: {actividad}

Generá un plan de comidas completo para 7 días (lunes a domingo) con las siguientes comidas diarias:
1. Desayuno
2. Almuerzo
3. Merienda
4. Cena

Requisitos del plan:
- Adaptado específicamente al perfil y objetivo del usuario
- Ingredientes accesibles en Argentina
- Porciones realistas y balanceadas
- Incluir una breve nota nutricional al final con los puntos clave del plan
- Formato claro y fácil de seguir

Respondé directamente con el plan sin preámbulos."""

        with st.spinner("🔄 Generando tu plan personalizado..."):
            try:
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # económico y eficiente
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=2000
                )
                plan = response.choices[0].message.content

                st.success("✅ ¡Plan generado exitosamente!")
                st.markdown("---")
                st.subheader("🗓️ Tu plan de alimentación semanal")
                st.markdown(plan)

                # Botón de descarga
                st.download_button(
                    label="📥 Descargar plan en texto",
                    data=plan,
                    file_name="plan_nutria.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"❌ Error al conectar con la API: {str(e)}")

# ─── Sección "Cómo funciona" ─────────────────────────────────────────────────
st.markdown("---")
with st.expander("❓ ¿Cómo funciona NutriIA?"):
    st.markdown("""
    <div class="info-card">
        <strong>1. Completá tu perfil</strong><br>
        Ingresá tus datos personales: edad, peso, altura, objetivo y restricciones alimentarias.
    </div>
    <div class="info-card">
        <strong>2. La IA construye tu prompt</strong><br>
        NutriIA arma automáticamente un prompt estructurado con tu información para enviarle a GPT-4.
    </div>
    <div class="info-card">
        <strong>3. Recibís tu plan en segundos</strong><br>
        GPT-4 genera un plan de 7 días con 4 comidas diarias, adaptado a tu perfil y usando ingredientes accesibles en Argentina.
    </div>
    <div class="info-card">
        <strong>4. Descargalo y usalo</strong><br>
        Podés descargar el plan en texto para guardarlo o imprimirlo.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    **⚠️ Importante:** NutriIA es una herramienta orientativa basada en IA. 
    No reemplaza la consulta con un profesional de la salud. 
    Ante dudas médicas, consultá con un nutricionista o médico.
    """)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    NutriIA · Proyecto Final CoderHouse · Prompt Engineering para Programadores<br>
    Lucas Romero · Comisión #86240 · 2025
</div>
""", unsafe_allow_html=True)
