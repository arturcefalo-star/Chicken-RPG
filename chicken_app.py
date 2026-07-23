import streamlit as st
import random

# Configuração da página
st.set_page_config(page_title="Chicken Slayer RPG", page_icon="🐔", layout="centered")

# --- TABELA DE RARIDADES E NOMES DE ARMAS ---
WEAPON_NAMES = {
    "Comum": ["Galho Seco", "Colher de Madeira", "Faca de Pão", "Espada Quebrada"],
    "Rara": ["Espada de Ferro", "Machado de Caça", "Clava de Bronze", "Daga Afiada"],
    "Épica": ["Lança de Aço", "Katana Penada", "Martelo do Trovão", "Lança-Chamas de Bolso"],
    "Lendária": ["Excalibur das Galinhas", "Matadora de Galos", "Foice Celestial", "Desintegrador de Penas"]
}

RARITY_COLORS = {
    "Comum": "⚪",
    "Rara": "🔵",
    "Épica": "🟣",
    "Lendária": "🟡"
}

# --- INICIALIZAÇÃO DO ESTADO DO JOGO ---
if "player" not in st.session_state:
    st.session_state.player = {
        "level": 1,
        "hp": 30,
        "max_hp": 30,
        "base_atk": 3,
        "weapon_atk": 2,
        "gold": 0,
        "weapon_name": "Espada de Madeira",
        "weapon_rarity": "Comum"
    }

if "wave" not in st.session_state:
    st.session_state.wave = 1
    st.session_state.kills_in_wave = 0
    st.session_state.kills_target = 25

if "enemy" not in st.session_state:
    st.session_state.enemy = None

if "log" not in st.session_state:
    st.session_state.log = ["Bem-vindo ao Chicken Slayer! Defenda-se contra a horda!"]

# --- FUNÇÕES DO JOGO ---
def log_msg(msg):
    st.session_state.log.insert(0, msg)

def get_player_total_atk():
    p = st.session_state.player
    return p["base_atk"] + p["weapon_atk"]

def generate_weapon_drop():
    # Sorteio de raridade baseada em probabilidades
    roll = random.random()
    if roll < 0.05:
        rarity = "Lendária"
        mult = 5
    elif roll < 0.15:
        rarity = "Épica"
        mult = 3
    elif roll < 0.40:
        rarity = "Rara"
        mult = 2
    else:
        rarity = "Comum"
        mult = 1

    # O dano escala com a raridade e a onda atual
    wave = st.session_state.wave
    atk = random.randint(2, 4) * mult + (wave * 2)
    name = random.choice(WEAPON_NAMES[rarity])
    
    return {"name": name, "rarity": rarity, "atk": atk}

def spawn_chicken():
    wave = st.session_state.wave
    
    # Onda 1 é exclusivamente contra Pintinhos
    if wave == 1:
        st.session_state.enemy = {
            "name": "Pintinho Amarelinho", 
            "hp": 12, 
            "max_hp": 12, 
            "atk": 2, 
            "gold": 5
        }
    else:
        # Ondas superiores liberam inimigos mais fortes
        scale = wave - 1
        types = [
            {"name": "Pintinho Amarelinho", "hp": 12 + (scale * 3), "atk": 2 + scale, "gold": 5},
            {"name": "Galinha Caipira", "hp": 25 + (scale * 5), "atk": 4 + scale, "gold": 12},
            {"name": "Galo Raivoso", "hp": 45 + (scale * 8), "atk": 7 + scale, "gold": 25},
            {"name": "Galinha Zumbi", "hp": 75 + (scale * 12), "atk": 12 + scale, "gold": 50},
        ]
        max_idx = min(wave - 1, len(types) - 1)
        selected = random.choice(types[:max_idx + 1])
        selected["max_hp"] = selected["hp"]
        st.session_state.enemy = selected.copy()

    log_msg(f"🐔 Um **{st.session_state.enemy['name']}** avançou na Onda {wave}!")

def check_wave_progress():
    st.session_state.kills_in_wave += 1
    
    if st.session_state.kills_in_wave >= st.session_state.kills_target:
        st.session_state.wave += 1
        st.session_state.kills_in_wave = 0
        
        # Bônus por passar de onda
        p = st.session_state.player
        p["level"] += 1
        p["max_hp"] += 15
        p["hp"] = p["max_hp"]
        p["base_atk"] += 2
        
        log_msg(f"🚨 **ONDA CONCLUÍDA!** Você sobreviveu e avançou para a **Onda {st.session_state.wave}**!")

if st.session_state.enemy is None:
    spawn_chicken()

def attack():
    p = st.session_state.player
    e = st.session_state.enemy

    if not e:
        return

    # Jogador ataca
    total_atk = get_player_total_atk()
    damage_to_e = max(1, total_atk + random.randint(-1, 2))
    e["hp"] -= damage_to_e
    log_msg(f"⚔️ Você causou {damage_to_e} de dano no {e['name']}!")

    # Inimigo Derrotado
    if e["hp"] <= 0:
        log_msg(f"💥 Você derrotou o {e['name']} e ganhou 💰 {e['gold']} moedas!")
        p["gold"] += e["gold"]
        
        # Lógica de Drop de Arma
        if random.random() < 0.45:  # 45% de chance de dropar uma arma ao matar
            drop = generate_weapon_drop()
            rar_icon = RARITY_COLORS[drop["rarity"]]
            
            log_msg(f"🎁 **DROP!** A galinha deixou cair: {rar_icon} **{drop['name']}** ({drop['rarity']}) com +{drop['atk']} Dano!")
            
            # Equipar automaticamente se for mais forte
            if drop["atk"] > p["weapon_atk"]:
                p["weapon_atk"] = drop["atk"]
                p["weapon_name"] = drop["name"]
                p["weapon_rarity"] = drop["rarity"]
                log_msg(f"✨ **EQUIPADA!** Você equipou a nova arma!")

        check_wave_progress()
        spawn_chicken()
        return

    # Inimigo contra-ataca
    damage_to_p = max(1, e["atk"] + random.randint(-1, 1))
    p["hp"] -= damage_to_p
    log_msg(f"🐔 O {e['name']} te atacou causando {damage_to_p} de dano!")

    # Game Over
    if p["hp"] <= 0:
        p["hp"] = p["max_hp"]
        p["gold"] = max(0, p["gold"] - 15)
        log_msg("☠️ **VOCÊ FOI DERROTADO!** Sua vida foi restaurada na Hospedaria (Perdeu 15 moedas).")
        spawn_chicken()

# --- INTERFAÇAS DO STREAMLIT ---
st.title("🐔 Chicken Slayer: Hordas")

# Painel Superior (Status)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Onda Atual", f"🌊 {st.session_state.wave}")
col2.metric("Progresso da Onda", f"🎯 {st.session_state.kills_in_wave}/{st.session_state.kills_target}")
col3.metric("Vida (HP)", f"❤️ {st.session_state.player['hp']}/{st.session_state.player['max_hp']}")
col4.metric("Dano Total", f"🗡️ {get_player_total_atk()}")

# Status da Arma Atual
p = st.session_state.player
rar_icon = RARITY_COLORS[p['weapon_rarity']]
st.caption(f"**Arma Equipada:** {rar_icon} {p['weapon_name']} ({p['weapon_rarity']}) — Bonus: +{p['weapon_atk']} Dano | **Ouro:** 💰 {p['gold']}")

st.divider()

# Layout Principal
tab_battle, tab_shop = st.tabs(["⚔️ Combate da Onda", "🏪 Hospedaria"])

with tab_battle:
    e = st.session_state.enemy
    st.subheader(f"Inimigo: {e['name']}")
    
    # Barra de Vida do Inimigo
    hp_percent = max(0.0, float(e["hp"] / e["max_hp"]))
    st.progress(hp_percent, text=f"HP do Inimigo: {e['hp']}/{e['max_hp']}")

    col_atk, col_flee = st.columns(2)
    if col_atk.button("🗡️ Atacar", type="primary", use_container_width=True):
        attack()
        st.rerun()
        
    if col_flee.button("🏃 Trocar de Alvo", use_container_width=True):
        log_msg("🏃 Você desviou e procurou outro alvo na horda!")
        spawn_chicken()
        st.rerun()

with tab_shop:
    st.subheader("🏥 Hospedaria")
    if st.button("💤 Curar Vida Toda (10 Moedas)", use_container_width=True):
        if st.session_state.player["gold"] >= 10:
            st.session_state.player["gold"] -= 10
            st.session_state.player["hp"] = st.session_state.player["max_hp"]
            log_msg("✨ Você descansou e recuperou toda a sua vida!")
            st.rerun()
        else:
            st.error("Ouro insuficiente!")

st.divider()

# Histórico/Log
st.subheader("📜 Histórico da Batalha")
for item in st.session_state.log[:6]:
    st.write(item)
