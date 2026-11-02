
import streamlit as st

st.set_page_config(
    page_title="Mining Game",
    page_icon="⛏️",
    layout="centered"
)

picaretas = [
    {"nome": "Wood Pickaxe", "preco": 0, "poder": 1, "cor": (130,75,30)},
    {"nome": "Stone Pickaxe", "preco": 180, "poder": 3, "cor": (140,140,140)},
    {"nome": "Copper Pickaxe", "preco": 650, "poder": 6, "cor": (190,110,60)},
    {"nome": "Gold Pickaxe", "preco": 1800, "poder": 10, "cor": (255,215,55)},
    {"nome": "Iron Pickaxe", "preco": 4200, "poder": 15, "cor": (190,190,210)},
    {"nome": "Diamond Pickaxe", "preco": 9000, "poder": 22, "cor": (0,220,255)},
    {"nome": "Obsidian Pickaxe", "preco": 18000, "poder": 31, "cor": (55,35,80)},
    {"nome": "Ruby Pickaxe", "preco": 35000, "poder": 42, "cor": (220,20,60)},
    {"nome": "Emerald Pickaxe", "preco": 65000, "poder": 56, "cor": (0,200,90)},
    {"nome": "Amethyst Pickaxe", "preco": 110000, "poder": 73, "cor": (150,70,220)},
    {"nome": "Sapphire Pickaxe", "preco": 180000, "poder": 94, "cor": (30,100,255)},
    {"nome": "Titanium Pickaxe", "preco": 290000, "poder": 120, "cor": (160,180,190)},
    {"nome": "Cobalt Pickaxe", "preco": 460000, "poder": 151, "cor": (20,70,180)},
    {"nome": "Uranium Pickaxe", "preco": 720000, "poder": 189, "cor": (120,255,20)},
    {"nome": "Plasma Pickaxe", "preco": 1100000, "poder": 235, "cor": (0,255,220)},
    {"nome": "Void Pickaxe", "preco": 1650000, "poder": 290, "cor": (65,0,110)},
    {"nome": "Meteor Pickaxe", "preco": 2400000, "poder": 355, "cor": (110,75,65)},
    {"nome": "Magma Pickaxe", "preco": 3400000, "poder": 430, "cor": (255,75,0)},
    {"nome": "Crystal Pickaxe", "preco": 4800000, "poder": 520, "cor": (130,220,255)},
    {"nome": "Ancient Pickaxe", "preco": 6700000, "poder": 630, "cor": (180,150,90)},
    {"nome": "Dragon Pickaxe", "preco": 9200000, "poder": 760, "cor": (180,20,20)},
    {"nome": "Celestial Pickaxe", "preco": 12500000, "poder": 910, "cor": (255,240,160)},
    {"nome": "Quantum Pickaxe", "preco": 17000000, "poder": 1080, "cor": (0,255,180)},
    {"nome": "Galactic Pickaxe", "preco": 23000000, "poder": 1280, "cor": (100,50,220)},
    {"nome": "Eternity Pickaxe", "preco": 31000000, "poder": 1510, "cor": (255,100,200)},
    {"nome": "Infinity Pickaxe", "preco": 42000000, "poder": 1780, "cor": (255,255,255)}
]

minerios = [
    {"nome": "Stone", "preco": 0, "multiplicador": 1, "cor": (110,110,110)},
    {"nome": "Coal", "preco": 100, "multiplicador": 1.5, "cor": (30,30,30)},
    {"nome": "Copper", "preco": 400, "multiplicador": 2, "cor": (190,110,60)},
    {"nome": "Gold", "preco": 1200, "multiplicador": 2.5, "cor": (255,215,55)},
    {"nome": "Iron", "preco": 3000, "multiplicador": 3, "cor": (190,190,210)},
    {"nome": "Diamond", "preco": 7000, "multiplicador": 3.5, "cor": (0,220,255)},
    {"nome": "Obsidian", "preco": 15000, "multiplicador": 4, "cor": (55,35,80)},
    {"nome": "Ruby", "preco": 30000, "multiplicador": 4.5, "cor": (220,20,60)},
    {"nome": "Emerald", "preco": 55000, "multiplicador": 5, "cor": (0,200,90)},
    {"nome": "Amethyst", "preco": 95000, "multiplicador": 5.5, "cor": (150,70,220)},
    {"nome": "Sapphire", "preco": 160000, "multiplicador": 6, "cor": (30,100,255)},
    {"nome": "Titanium", "preco": 260000, "multiplicador": 6.5, "cor": (160,180,190)},
    {"nome": "Cobalt", "preco": 420000, "multiplicador": 7, "cor": (20,70,180)},
    {"nome": "Uranium", "preco": 680000, "multiplicador": 7.5, "cor": (120,255,20)},
    {"nome": "Plasma", "preco": 1050000, "multiplicador": 8, "cor": (0,255,220)},
    {"nome": "Void", "preco": 1600000, "multiplicador": 8.5, "cor": (65,0,110)},
    {"nome": "Meteorite", "preco": 2200000, "multiplicador": 9, "cor": (110,75,65)},
    {"nome": "Magma", "preco": 3100000, "multiplicador": 9.5, "cor": (255,75,0)},
    {"nome": "Crystal", "preco": 4400000, "multiplicador": 10, "cor": (130,220,255)},
    {"nome": "Ancient Ore", "preco": 6200000, "multiplicador": 10.5, "cor": (180,150,90)},
    {"nome": "Dragonite", "preco": 8700000, "multiplicador": 11, "cor": (180,20,20)},
    {"nome": "Celestite", "preco": 12000000, "multiplicador": 11.5, "cor": (255,240,160)},
    {"nome": "Quantum Ore", "preco": 16500000, "multiplicador": 12, "cor": (0,255,180)},
    {"nome": "Galactium", "preco": 22500000, "multiplicador": 12.5, "cor": (100,50,220)},
    {"nome": "Eternium", "preco": 30000000, "multiplicador": 13, "cor": (255,100,200)},
    {"nome": "Infinity Ore", "preco": 40000000, "multiplicador": 13.5, "cor": (255,255,255)}
]

if "moedas" not in st.session_state:
    st.session_state.moedas = 0
    st.session_state.picaretas_compradas = [0]
    st.session_state.minerios_comprados = [0]
    st.session_state.picareta_atual = 0
    st.session_state.minerio_atual = 0
    st.session_state.recompensa = 0

s = st.session_state

def formatar(valor):
    return f"{valor:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.markdown("""
<style>
.stApp {
    background: #101014;
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
div.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 10px;
    font-weight: bold;
}
.minerio {
    width: 150px;
    height: 150px;
    margin: 15px auto;
    border-radius: 12px;
    border: 4px solid #555;
    box-shadow: 0 0 20px #333;
}
</style>
""", unsafe_allow_html=True)

st.title("⛏️ MINING GAME")

st.metric("💰 MOEDAS", "$ " + formatar(s.moedas))

picareta = picaretas[s.picareta_atual]
minerio = minerios[s.minerio_atual]

r, g, b = minerio["cor"]
cor_bloco = f"rgb({r},{g},{b})"

st.markdown(
    f'<div class="minerio" style="background:{cor_bloco}"></div>',
    unsafe_allow_html=True
)

st.markdown(
    f"<center><b>{minerio['nome']}</b></center>",
    unsafe_allow_html=True
)

st.markdown(
    f"<center>⛏️ {picareta['nome']}</center>",
    unsafe_allow_html=True
)

if st.button("⛏️ MINERAR", use_container_width=True):
    s.recompensa = picareta["poder"] * minerio["multiplicador"]
    s.moedas += s.recompensa
    st.rerun()

if s.recompensa > 0:
    st.success("+$ " + formatar(s.recompensa))

st.divider()

st.subheader("🛒 SHOP")

aba = st.radio(
    "Categoria",
    ["Picaretas", "Minérios"],
    horizontal=True
)

if aba == "Picaretas":
    opcoes = list(range(1, len(picaretas)))
    indice = st.selectbox(
        "Escolha uma picareta",
        opcoes,
        format_func=lambda i: picaretas[i]["nome"]
    )

    item = picaretas[indice]
    st.markdown(f"### {item['nome']}")
    st.write("⚡ Poder:", item["poder"])
    st.write("💰 Preço: $", formatar(item["preco"]))

    if indice in s.picaretas_compradas:
        if s.picareta_atual == indice:
            st.success("Picareta equipada")
        elif st.button("EQUIPAR PICARETA"):
            s.picareta_atual = indice
            st.rerun()
    else:
        if st.button("COMPRAR PICARETA"):
            if s.moedas >= item["preco"]:
                s.moedas -= item["preco"]
                s.picaretas_compradas.append(indice)
                s.picareta_atual = indice
                st.rerun()
            else:
                st.error("Moedas insuficientes!")

else:
    opcoes = list(range(len(minerios)))
    indice = st.selectbox(
        "Escolha um minério",
        opcoes,
        format_func=lambda i: minerios[i]["nome"]
    )

    item = minerios[indice]
    st.markdown(f"### {item['nome']}")
    st.write("✨ Multiplicador:", str(item["multiplicador"]) + "x")
    st.write("💰 Preço: $", formatar(item["preco"]))

    if indice in s.minerios_comprados:
        if s.minerio_atual == indice:
            st.success("Minério equipado")
        elif st.button("EQUIPAR MINÉRIO"):
            s.minerio_atual = indice
            st.rerun()
    else:
        if st.button("COMPRAR MINÉRIO"):
            if s.moedas >= item["preco"]:
                s.moedas -= item["preco"]
                s.minerios_comprados.append(indice)
                s.minerio_atual = indice
                st.rerun()
            else:
                st.error("Moedas insuficientes!")

st.divider()

st.caption("Mining Game • Versão de navegador")
