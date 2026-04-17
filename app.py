"""
NutriIA - Asistente de Alimentación Personalizada con IA
Proyecto Final - Prompt Engineering para Programadores | CoderHouse
Autor: Lucas Romero | Comisión: #86240
"""

import streamlit as st
import google.generativeai as genai

# ─── Configuración de página ────────────────────────────────────────────────
st.set_page_config(page_title="NutriIA", page_icon="🥗", layout="centered")

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2ecc71, #27ae60);
        padding: 2rem; border-radius: 12px;
        text-align: center; color: white; margin-bottom: 2rem;
    }
    .main-header h1 { font-size: 2.5rem; margin: 0; }
    .main-header p  { font-size: 1.1rem; margin: 0.5rem 0 0; opacity: 0.9; }
    .info-card {
        background: #f8f9fa; border-left: 4px solid #2ecc71;
        border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 0.8rem;
    }
    .footer {
        text-align: center; color: #888; font-size: 0.85rem;
        margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🥗 NutriIA</h1>
    <p>Tu nutricionista virtual · Planes de alimentación personalizados con IA</p>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuración")
    api_key = st.text_input("Google Gemini API Key", type="password", placeholder="AIza...")
    st.markdown("Obtené tu key gratis en [aistudio.google.com](https://aistudio.google.com/apikey)")
    st.markdown("---")
    st.markdown("**NutriIA** genera planes de comidas semanales personalizados usando Gemini.")
    st.markdown("*Comisión #86240 · Lucas Romero*")

# ─── Formulario ──────────────────────────────────────────────────────────────
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

actividad = st.select_slider(
    "Nivel de actividad física",
    options=["Sedentario", "Ligero (1-2 días/semana)", "Moderado (3-4 días/semana)", "Activo (5+ días/semana)"]
)

# ─── Botón ───────────────────────────────────────────────────────────────────
st.markdown("---")
generar = st.button("🚀 Generar mi plan semanal", use_container_width=True, type="primary")

if generar:
    if not api_key:
        st.error("⚠️ Ingresá tu Gemini API Key en el panel lateral para continuar.")
    else:
        restricciones_str = ", ".join(restricciones) if restricciones else "Ninguna"
        prompt = f"""Eres un nutricionista experto. El usuario tiene los siguientes datos:
- Edad: {edad} años
- Sexo: {sexo}
- Peso: {peso} kg
- Altura: {altura} cm
- Objetivo: {objetivo}
- Restricciones alimentarias: {restricciones_str}
- Nivel de actividad física: {actividad}

Generá un plan de comidas completo para 7 días (lunes a domingo) con desayuno, almuerzo, merienda y cena.
Requisitos:
- Adaptado al perfil y objetivo del usuario
- Ingredientes accesibles en Argentina
- Porciones realistas y balanceadas
- Incluir una breve nota nutricional al final
Respondé directamente con el plan sin preámbulos."""

        with st.spinner("🔄 Generando tu plan personalizado..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content(prompt)
                plan = response.text

                st.success("✅ ¡Plan generado exitosamente!")
                st.markdown("---")
                st.subheader("🗓️ Tu plan de alimentación semanal")
                st.markdown(plan)
                st.download_button(
                    label="📥 Descargar plan en texto",
                    data=plan,
                    file_name="plan_nutria.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"❌ Error al conectar con la API: {str(e)}")

# ─── Cómo funciona ───────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("❓ ¿Cómo funciona NutriIA?"):
    st.markdown("""
    <div class="info-card"><strong>1. Completá tu perfil</strong><br>
    Ingresá tus datos personales: edad, peso, altura, objetivo y restricciones alimentarias.</div>
    <div class="info-card"><strong>2. La IA construye tu prompt</strong><br>
    NutriIA arma automáticamente un prompt estructurado con tu información para enviarle a Gemini.</div>
    <div class="info-card"><strong>3. Recibís tu plan en segundos</strong><br>
    Gemini genera un plan de 7 días con 4 comidas diarias, adaptado a tu perfil y usando ingredientes accesibles en Argentina.</div>
    <div class="info-card"><strong>4. Descargalo y usalo</strong><br>
    Podés descargar el plan en texto para guardarlo o imprimirlo.</div>
    """, unsafe_allow_html=True)
    st.markdown("**⚠️ Importante:** NutriIA es una herramienta orientativa. No reemplaza la consulta con un profesional de la salud.")

st.markdown("""
<div class="footer">
    NutriIA · Proyecto Final CoderHouse · Prompt Engineering para Programadores<br>
    Lucas Romero · Comisión #86240 · 2025
</div>
""", unsafe_allow_html=True)
