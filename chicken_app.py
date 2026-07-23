import streamlit as st
import random
import time

# Configuração da página
st.set_page_config(page_title="Chicken Slayer RPG", page_icon="🐔", layout="centered")

# --- TABELA DE RARIDADES E ARMAMENTO ---
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
    st.session_state.log = ["Bem-vindo ao Chicken Slayer! Prepare-se para enfrentar a horda."]

if "last_drop_msg" not in st.session_state:
    st.session_state.last_drop_msg = None

# --- FUNÇÕES DO JOGO ---
def log_msg(msg):
    st.session_state.log.insert(0, msg)

def get_player_total_atk():
    p = st.session_state.player
    return p["base_atk"] + p["weapon_atk"]

def generate_weapon_drop():
    wave = st.session_state.wave
    
    # A probabilidade de obter armas raras cresce com as ondas
    roll = random.random()
    if roll < (0.05 + wave * 0.01):
        rarity = "Lendária"
        mult = 5
    elif roll < (0.20 + wave * 0.02):
        rarity = "Épica"
        mult = 3
    elif roll < (0.50 + wave * 0.02):
        rarity = "Rara"
        mult = 2
    else:
        rarity = "Comum"
        mult = 1

    # Dano base aumenta significativamente a cada nova onda
    base_bonus = wave * 3
    atk = random.randint(2, 5) * mult + base_bonus
    name = random.choice(WEAPON_NAMES[rarity])
    
    return {"name": name, "rarity": rarity, "atk": atk}

def spawn_chicken():
    wave = st.session_state.wave
    
    if wave == 1:
        st.session_state.enemy = {
            "name": "Pintinho Amarelinho", 
            "hp": 12, 
            "max_hp": 12, 
            "atk": 2, 
            "gold": 5
        }
    else:
        # Galinhas ficam mais fortes (HP, Dano e Recompensas sobem com a onda)
        hp_boost = (wave - 1) * 10
        atk_boost = (wave - 1) * 3
        gold_boost = (wave - 1) * 6
        
        types = [
            {"name": f"Pintinho da Onda {wave}", "hp": 12 + hp_boost, "atk": 2 + atk_boost, "gold": 5 + gold_boost},
            {"name": f"Galinha Guerreira (Onda {wave})", "hp": 25 + hp_boost, "atk": 4 + atk_boost, "gold": 12 + gold_boost},
            {"name": f"Galo Blindado (Onda {wave})", "hp": 45 + hp_boost, "atk": 7 + atk_boost, "gold": 25 + gold_boost},
            {"name": f"Galinha Mutante (Onda {wave})", "hp": 75 + hp_boost, "atk": 12 + atk_boost, "gold": 50 + gold_boost},
        ]
        
        # Sorteia uma variante fortalecida
        selected = random.choice(types).copy()
        selected["max_hp"] = selected["hp"]
        st.session_state.enemy = selected

    log_msg(f"🐔 Um **{st.session_state.enemy['name']}** apareceu na Onda {wave}!")

def check_wave_progress():
    st.session_state.kills_in_wave += 1
    
    if st.session_state.kills_in_wave >= st.session_state.kills_target:
        st.session_state.wave += 1
        st.session_state.kills_in_wave = 0
        
        p = st.session_state.player
        p["level"] += 1
        p["max_hp"] += 20
        p["hp"] = p["max_hp"]
        p["base_atk"] += 3
        
        log_msg(f"🚨 **NOVA ONDA CHEGOU!** Você avançou para a **Onda {st.session_state.wave}**! As galinhas ficaram mais fortes e os drops melhores!")

if st.session_state.enemy is None:
    spawn_chicken()

def attack():
    # Cooldown simples para evitar ataques desenfreados
    time.sleep(0.3)
    
    p = st.session_state.player
    e = st.session_state.enemy

    if not e:
        return

    # Ataque do Jogador
    total_atk = get_player_total_atk()
    damage_to_e = max(1, total_atk + random.randint(-1, 2))
    e["hp"] -= damage_to_e
    log_msg(f"⚔️ Você atacou o {e['name']} causando {damage_to_e} de dano!")

    # Morte do Inimigo
    if e["hp"] <= 0:
        log_msg(f"💥 Você derrotou o {e['name']} e ganhou 💰 {e['gold']} moedas!")
        p["gold"] += e["gold"]
        
        # Sistema de Drop com aviso
        if random.random() < 0.50:  # 50% de chance de drop
            drop = generate_weapon_drop()
            rar_icon = RARITY_COLORS[drop["rarity"]]
            
            # Se for superior, equipa e gera notificação
            if drop["atk"] > p["weapon_atk"]:
                p["weapon_atk"] = drop["atk"]
                p["weapon_name"] = drop["name"]
                p["weapon_rarity"] = drop["rarity"]
                
                drop_msg = f"🎉 NOVO DROP EQUIPADO! {rar_icon} {drop['name']} ({drop['rarity']}) com +{drop['atk']} de Dano!"
                st.session_state.last_drop_msg = drop_msg
                log_msg(f"✨ **EQUIPADA!** {drop_msg}")
            else:
                log_msg(f"🗑️ A galinha dropou {rar_icon} **{drop['name']}** (+{drop['atk']} Dano), mas sua arma atual é melhor.")

        check_wave_progress()
        spawn_chicken()
        return

    # Contra-Ataque da Galinha
    damage_to_p = max(1, e["atk"] + random.randint(-1, 1))
    p["hp"] -= damage_to_p
    log_msg(f"🐔 O {e['name']} contra-atacou causando {damage_to_p} de dano!")

    # Derrota
    if p["hp"] <= 0:
        p["hp"] = p["max_hp"]
        p["gold"] = max(0, p["gold"] - 15)
        log_msg("☠️ **VOCÊ FOI DERROTADO!** Sua vida foi restaurada na Hospedaria (Perdeu 15 moedas).")
        spawn_chicken()

# --- INTERFACE DO STREAMLIT ---
st.title("🐔 Chicken Slayer: Hordas")

# Notificação de Novo Drop Equipado
if st.session_state.last_drop_msg:
    st.toast(st.session_state.last_drop_msg, icon="🎁")
    st.success(st.session_state.last_drop_msg)
    st.session_state.last_drop_msg = None  # Limpa o aviso para a próxima rodada

# Painel Superior (Status)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Onda Atual", f"🌊 {st.session_state.wave}")
col2.metric("Progresso da Onda", f"🎯 {st.session_state.kills_in_wave}/{st.session_state.kills_target}")
col3.metric("Vida (HP)", f"❤️ {st.session_state.player['hp']}/{st.session_state.player['max_hp']}")
col4.metric("Dano Total", f"🗡️ {get_player_total_atk()}")

# Status do Equipamento Atual
p = st.session_state.player
rar_icon = RARITY_COLORS[p['weapon_rarity']]
st.caption(f"**Arma Equipada:** {rar_icon} **{p['weapon_name']}** ({p['weapon_rarity']}) — Bônus: +{p['weapon_atk']} Dano | **Ouro:** 💰 {p['gold']}")

st.divider()

# Layout Principal
tab_battle, tab_shop = st.tabs(["⚔️ Combate da Onda", "🏪 Hospedaria"])

with tab_battle:
    e = st.session_state.enemy
    st.subheader(f"Inimigo: {e['name']}")
    
    # Barra de Vida do Inimigo
    hp_percent = max(0.0, float(e["hp"] / e["max_hp"]))
    st.progress(hp_percent, text=f"HP do Inimigo: {e['hp']}/{e['max_hp']} | Ataque: ⚔️ {e['atk']}")

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
