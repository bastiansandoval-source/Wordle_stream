import random
import streamlit as st

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(page_title="Wordle en Streamlit", page_icon="🟩", layout="centered")

PALABRAS = [
    "CLIMA", "NUBES", "SOLAR", "FLORA", "FAUNA", "SUELO", "AGUAS", "OZONO",
    "NIEVE", "CALOR", "VAPOR", "GASES", "CICLO", "SELVA", "PRADO", "MONTE",
    "CERRO", "PLAYA", "ROCAS", "ARENA", "RIOS",  "LAGOS", "MARES", "CAMPO",
    "DELTA", "HUMOS", "FUEGO", "LLANO", "VALLE", "ISLAS", "COSTA", "ARBOL",
    "HOJAS", "TRIGO", "PESCA", "HIELO", "BRUMA", "RIEGO", "VERDE", "ESMOG"
    "ALGAS", "HONGO", "RAMAS", "LLUVIA", "DUNAS", "CAUCE", "FANGO", "POLEN",
    "RAYOS", "FRUTO", "VIENTO", "BRISA", "BARRO", "PINOS", "BROTE", "SAVIA",
    "LINCE", "COBRE", "MUSGO", "POZOS", "ABONO", "CERRO","BARRO", "BOLDO","CORAL"
]

MAX_INTENTOS = 6
LARGO_PALABRA = 5

# Dejamos solo palabras de 5 letras para esta primera versión
PALABRAS_VALIDAS = [p for p in PALABRAS if len(p) == LARGO_PALABRA]


# =========================
# ESTADO DEL JUEGO
# =========================
def iniciar_juego():
    st.session_state.palabra_secreta = random.choice(PALABRAS_VALIDAS)
    st.session_state.intentos = []
    st.session_state.juego_terminado = False
    st.session_state.gano = False


if "palabra_secreta" not in st.session_state:
    iniciar_juego()


# =========================
# LÓGICA WORDLE
# =========================
def evaluar_intento(secreta: str, intento: str):
    """
    Devuelve una lista de estados por letra:
    - correcta: letra correcta en lugar correcto
    - presente: letra está en la palabra pero en otra posición
    - ausente: letra no está en la palabra
    """
    resultado = ["ausente"] * LARGO_PALABRA
    letras_restantes = list(secreta)

    # Primera pasada: marcar correctas
    for i in range(LARGO_PALABRA):
        if intento[i] == secreta[i]:
            resultado[i] = "correcta"
            letras_restantes[i] = None

    # Segunda pasada: marcar presentes
    for i in range(LARGO_PALABRA):
        if resultado[i] == "correcta":
            continue

        if intento[i] in letras_restantes:
            resultado[i] = "presente"
            indice = letras_restantes.index(intento[i])
            letras_restantes[indice] = None

    return resultado


# =========================
# ESTILOS CSS
# =========================
st.markdown(
    """
    <style>
    .titulo {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitulo {
        text-align: center;
        color: #bbbbbb;
        margin-bottom: 1.5rem;
    }

    .fila {
        display: grid;
        grid-template-columns: repeat(5, 62px);
        gap: 6px;
        justify-content: center;
        margin-bottom: 6px;
    }

    .casilla {
        width: 62px;
        height: 62px;
        border: 2px solid #3a3a3c;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.9rem;
        font-weight: bold;
        text-transform: uppercase;
        background-color: #121213;
        color: white;
    }

    .correcta {
        background-color: #538d4e;
        border-color: #538d4e;
    }

    .presente {
        background-color: #b59f3b;
        border-color: #b59f3b;
    }

    .ausente {
        background-color: #3a3a3c;
        border-color: #3a3a3c;
    }

    .vacia {
        background-color: #121213;
        border-color: #3a3a3c;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================
# INTERFAZ
# =========================
st.markdown("""
<style>
.titulo {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #4CAF50;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)
st.markdown('<div class="titulo">🌎 Wordle: Medio Ambiente</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Adivina la palabra de 5 letras</div>', unsafe_allow_html=True)

#st.markdown('<div class="titulo">Wordle: Medio Ambiente </div>', unsafe_allow_html=True)
#st.markdown('<div style="color: green; font-size:40px;">Wordle: Medio Ambiente</div>', unsafe_allow_html=True)

def dibujar_tablero():
    html = ""

    for fila_num in range(MAX_INTENTOS):
        html += '<div class="fila">'

        if fila_num < len(st.session_state.intentos):
            palabra, evaluacion = st.session_state.intentos[fila_num]

            for letra, estado in zip(palabra, evaluacion):
                html += f'<div class="casilla {estado}">{letra}</div>'
        else:
            for _ in range(LARGO_PALABRA):
                html += '<div class="casilla vacia"></div>'

        html += '</div>'

    st.markdown(html, unsafe_allow_html=True)


# Mostrar tablero
dibujar_tablero()

# Mostrar input solo si el juego sigue activo
if not st.session_state.juego_terminado:
    intento_usuario = st.text_input(
        "Escribe una palabra de 5 letras:",
        max_chars=LARGO_PALABRA,
        key="entrada_usuario"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Enviar", use_container_width=True):
            intento = intento_usuario.strip().upper()

            if len(intento) != LARGO_PALABRA:
                st.warning("La palabra debe tener exactamente 5 letras.")
            elif not intento.isalpha():
                st.warning("Solo debes escribir letras.")
            elif intento not in PALABRAS_VALIDAS:
                st.warning("Esa palabra no está en la lista de palabras válidas de esta demo.")
            else:
                evaluacion = evaluar_intento(st.session_state.palabra_secreta, intento)
                st.session_state.intentos.append((intento, evaluacion))

                if intento == st.session_state.palabra_secreta:
                    st.session_state.juego_terminado = True
                    st.session_state.gano = True
                elif len(st.session_state.intentos) >= MAX_INTENTOS:
                    st.session_state.juego_terminado = True

                st.rerun()

    with col2:
        if st.button("Nuevo juego", use_container_width=True):
            iniciar_juego()
            st.rerun()

else:
    if st.session_state.gano:
        st.success("¡Ganaste! Adivinaste la palabra.")
    else:
        st.error(f"Perdiste. La palabra era: {st.session_state.palabra_secreta}")

    if st.button("Jugar otra vez", use_container_width=True):
        iniciar_juego()
        st.rerun()


# =========================
# AYUDA / EXPLICACIÓN
# =========================


with st.expander("Palabras válidas de esta demo"):
    st.write(", ".join(PALABRAS_VALIDAS))