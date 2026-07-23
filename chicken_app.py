import streamlit as st
import random

# Configuração da página
st.set_page_config(page_title="Chicken RPG", page_icon="🐔", layout="centered")

# --- INICIALIZAÇÃO DO ESTADO DO JOGO ---
if "player" not in st.session_state:
    st.session_state.player = {
        "level": 1,
        "hp": 30,
        "max_hp": 30,
        "atk": 5,
        "gold": 0,
        "weapon": "Espada de Madeira",
        "chickens_slain": 0
    }

if "enemy" not in st.session_state:
    st.session_state.enemy = None

if "log" not in st.session_state:
    st.session_state.log = ["Bem-vindo ao Chicken Slayer! Escolha caçar para encontrar uma galinha."]

# --- FUNÇÕES DO JOGO ---
def log_msg(msg):
    st.session_state.log.insert(0, msg)

def spawn_chicken():
    types = [
        {"name": "Pintinho Amarelinho", "hp": 10, "max_hp": 10, "atk": 2, "gold": 5, "xp": 10},
        {"name": "Galinha Caipira", "hp": 20, "max_hp": 20, "atk": 4, "gold": 12, "xp": 20},
        {"name": "Galo Raivoso", "hp": 35, "max_hp": 35, "atk": 7, "gold": 25, "xp": 40},
        {"name": "Galinha Zumbi", "hp": 60, "max_hp": 60, "atk": 12, "gold": 50, "xp": 80},
    ]
    # Escolhe a galinha com base no nível do jogador
    max_idx = min(st.session_state.player["level"], len(types)) - 1
    selected = random.choice(types[:max_idx + 1])
    st.session_state.enemy = selected.copy()
    log_msg(f"🐔 Um(a) **{selected['name']}** apareceu!")

def check_level_up():
    p = st.session_state.player
    # A cada 50 de ouro ganho equivalentemente podemos considerar nivel
    if p["chickens_slain"] >= p["level"] * 3:
        p["level"] += 1
        p["max_hp"] += 10
        p["hp"] = p["max_hp"]
        p["atk"] += 2
        log_msg(f"🎉 **SUBIU DE NÍVEL!** Você agora é Nível {p['level']}!")

def attack():
    p = st.session_state.player
    e = st.session_state.enemy

    if not e:
        return

    # Jogador ataca
    damage_to_e = max(1, p["atk"] + random.randint(-1, 2))
    e["hp"] -= damage_to_e
    log_msg(f"⚔️ Você atacou o {e['name']} causando {damage_to_e} de dano!")

    # Verifica se a galinha morreu
    if e["hp"] <= 0:
        log_msg(f"💥 Você derrotou o {e['name']} e ganhou 💰 {e['gold']} moedas!")
        p["gold"] += e["gold"]
        p["chickens_slain"] += 1
        st.session_state.enemy = None
        check_level_up()
        return

    # Galinha contra-ataca
    damage_to_p = max(1, e["atk"] + random.randint(-1, 1))
    p["hp"] -= damage_to_p
    log_msg(f"🐔 O {e['name']} te bicou e causou {damage_to_p} de dano!")

    # Game Over
    if p["hp"] <= 0:
        p["hp"] = 0
        log_msg("☠️ **VOCÊ MORREU!** As galinhas dominaram... O jogo foi reiniciado.")
        # Reset rápido
        p["hp"] = p["max_hp"]
        p["gold"] = max(0, p["gold"] - 10)
        st.session_state.enemy = None

# --- INTERFAÇAS DO STREAMLIT ---
st.title("🐔 Chicken Slayer RPG")

# Painel Superior (Status)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Nível", st.session_state.player["level"])
col2.metric("Vida (HP)", f"{st.session_state.player['hp']}/{st.session_state.player['max_hp']}")
col3.metric("Ouro", f"💰 {st.session_state.player['gold']}")
col4.metric("Ataque", f"🗡️ {st.session_state.player['atk']}")

st.divider()

# Layout Principal: Esquerda (Combate), Direita (Loja/Hospedaria)
tab_battle, tab_shop = st.tabs(["⚔️ Caça & Combate", "🏪 Loja & Hospedaria"])

with tab_battle:
    if st.session_state.enemy is None:
        st.info("Nenhuma galinha por perto no momento.")
        if st.button("🔎 Procurar Galinha", use_container_width=True):
            spawn_chicken()
            st.rerun()
    else:
        e = st.session_state.enemy
        st.subheader(f"Inimigo: {e['name']}")
        
        # Barra de Vida do Inimigo
        hp_percent = max(0.0, float(e["hp"] / e["max_hp"]))
        st.progress(hp_percent, text=f"HP da Galinha: {e['hp']}/{e['max_hp']}")

        col_atk, col_run = st.columns(2)
        if col_atk.button("🗡️ Atacar", type="primary", use_container_width=True):
            attack()
            st.rerun()
        if col_run.button("🏃 Fugir", use_container_width=True):
            st.session_state.enemy = None
            log_msg("🏃 Você fugiu da batalha!")
            st.rerun()

with tab_shop:
    st.subheader("🏥 Hospedaria")
    if st.button("💤 Descansar na Hospedaria (10 Moedas)", use_container_width=True):
        if st.session_state.player["gold"] >= 10:
            st.session_state.player["gold"] -= 10
            st.session_state.player["hp"] = st.session_state.player["max_hp"]
            log_msg("✨ Você descansou e recuperou toda a sua vida!")
            st.rerun()
        else:
            st.error("Ouro insuficiente!")

    st.subheader("🗡️ Ferreiro")
    weapons = [
        {"name": "Espada de Ferro", "atk": 10, "cost": 30},
        {"name": "Machado Matador de Galinhas", "atk": 18, "cost": 80},
        {"name": "Lança-Lança-Chamas", "atk": 30, "cost": 200},
    ]

    for w in weapons:
        col_w1, col_w2 = st.columns([2, 1])
        col_w1.write(f"**{w['name']}** (+{w['atk']} Dano)")
        if col_w2.button(f"Comprar ({w['cost']} 💰)", key=w['name']):
            if st.session_state.player["gold"] >= w['cost']:
                st.session_state.player["gold"] -= w['cost']
                st.session_state.player["atk"] += w['atk']
                st.session_state.player["weapon"] = w['name']
                log_msg(f"🛒 Você comprou {w['name']}!")
                st.rerun()
            else:
                st.error("Ouro insuficiente!")

st.divider()

# Histórico/Log
st.subheader("📜 Histórico de Ações")
for item in st.session_state.log[:5]:  # Mostra as últimas 5 ações
    st.write(item)
