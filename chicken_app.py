import streamlit as st
import random
import time

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

CHICKEN_SPECIES = [
    {"name": "Pintinho Amarelinho", "icon": "🐥"},
    {"name": "Galinha Caipira de Brigas", "icon": "🐔"},
    {"name": "Galo Cego da Madrugada", "icon": "🐓"},
    {"name": "Galinha Cibernética", "icon": "🤖🐔"},
    {"name": "Super Galinha Zumbi", "icon": "🧟🐔"},
    {"name": "Galo Mutante do Apocalipse", "icon": "🔥🐓"},
    {"name": "Imperatriz das Galinhas", "icon": "👑🐔"},
]

# --- INICIALIZAÇÃO DO ESTADO DO JOGO ---
if "player" not in st.session_state:
    st.session_state.player = {
        "hp": 30,
        "max_hp": 30,
        "base_atk": 3,
        "weapon_atk": 2,
        "weapon_level": 0,
        "gold": 0,
        "weapon_name": "Espada de Madeira",
        "weapon_rarity": "Comum"
    }

if "wave" not in st.session_state:
    st.session_state.wave = 1
    st.session_state.kills_in_wave = 0

if "enemy" not in st.session_state:
    st.session_state.enemy = None

if "notice_text" not in st.session_state:
    st.session_state.notice_text = None

if "notice_time" not in st.session_state:
    st.session_state.notice_time = 0.0

if "is_respawning" not in st.session_state:
    st.session_state.is_respawning = False

DEATH_COOLDOWN = 1.5

# --- FUNÇÕES DO JOGO ---
def set_notice(text):
    """Define um aviso que dura 5 segundos sem sumir no clique"""
    st.session_state.notice_text = text
    st.session_state.notice_time = time.time()

def get_wave_target(wave):
    return wave * 25

def get_player_total_atk():
    p = st.session_state.player
    return p["base_atk"] + p["weapon_atk"] + (p["weapon_level"] * 3)

def generate_weapon_drop():
    wave = st.session_state.wave
    
    roll = random.random()
    if roll < (0.05 + wave * 0.015):
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

    base_bonus = wave * 3
    atk = random.randint(2, 5) * mult + base_bonus
    name = random.choice(WEAPON_NAMES[rarity])
    
    return {"name": name, "rarity": rarity, "atk": atk}

def spawn_wave_chicken():
    wave = st.session_state.wave
    species_idx = min(wave - 1, len(CHICKEN_SPECIES) - 1)
    species_info = CHICKEN_SPECIES[species_idx]
    
    fixed_hp = 18 + (wave - 1) * 15
    fixed_atk = 2 + (wave - 1) * 2
    fixed_gold = 5 + (wave - 1) * 4

    name = f"{species_info['icon']} {species_info['name']}"
    
    st.session_state.enemy = {
        "name": name,
        "hp": fixed_hp,
        "max_hp": fixed_hp,
        "atk": fixed_atk,
        "gold": fixed_gold
    }

if st.session_state.enemy is None:
    spawn_wave_chicken()

def animate_health_bar(progress_container, start_hp, end_hp, max_hp, enemy_atk):
    steps = 8
    start_hp = max(0, start_hp)
    end_hp = max(0, end_hp)
    
    for i in range(steps + 1):
        current_hp = start_hp - ((start_hp - end_hp) * (i / steps))
        current_hp_display = max(0, int(current_hp))
        hp_percent = max(0.0, float(current_hp_display / max_hp))
        
        progress_container.progress(
            hp_percent, 
            text=f"HP da Galinha: {current_hp_display}/{max_hp} | Dano: ⚔️ {enemy_atk}"
        )
        time.sleep(0.015)

def attack(progress_container):
    p = st.session_state.player
    e = st.session_state.enemy

    if not e or st.session_state.is_respawning:
        return

    total_atk = get_player_total_atk()
    damage_to_e = max(1, total_atk + random.randint(-1, 2))
    
    old_hp = max(0, e["hp"])
    e["hp"] = max(0, e["hp"] - damage_to_e)

    animate_health_bar(progress_container, old_hp, e["hp"], e["max_hp"], e["atk"])

    if e["hp"] <= 0:
        p["gold"] += e["gold"]
        st.session_state.kills_in_wave += 1
        
        # Testar Drop de Arma (40%)
        if random.random() < 0.40:
            drop = generate_weapon_drop()
            rar_icon = RARITY_COLORS[drop["rarity"]]
            
            if drop["atk"] > p["weapon_atk"]:
                p["weapon_atk"] = drop["atk"]
                p["weapon_name"] = drop["name"]
                p["weapon_rarity"] = drop["rarity"]
                p["weapon_level"] = 0
                
                set_notice(f"🎉 **NOVA ARMA EQUIPADA!** Dropou: {rar_icon} **{drop['name']}** (+{drop['atk']} Dano Base)!")
            else:
                set_notice(f"📦 Dropou {rar_icon} {drop['name']} (+{drop['atk']} Dano), mas sua arma atual é mais forte!")

        target = get_wave_target(st.session_state.wave)
        if st.session_state.kills_in_wave >= target:
            st.session_state.wave += 1
            st.session_state.kills_in_wave = 0
            p["max_hp"] += 10
            p["hp"] = p["max_hp"]
            set_notice(f"🚨 **ONDA CONCLUÍDA!** Avançou para a **Onda {st.session_state.wave}**!")

        st.session_state.is_respawning = True
        return

    damage_to_p = max(1, e["atk"] + random.randint(-1, 1))
    p["hp"] -= damage_to_p

    if p["hp"] <= 0:
        p["hp"] = p["max_hp"]
        p["gold"] = max(0, p["gold"] - 15)
        set_notice("☠️ Você foi derrotado! Vida restaurada (-15 moedas).")

# --- INTERFACE GRÁFICA ---
st.title("🐔 Chicken Slayer RPG")

wave_target = get_wave_target(st.session_state.wave)
p = st.session_state.player

# PAINEL SUPERIOR COM DESTAQUE DE DINHEIRO/OURO SEPARADO
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Onda", f"🌊 {st.session_state.wave}")
col2.metric("Abates", f"🎯 {st.session_state.kills_in_wave}/{wave_target}")
col3.metric("Vida", f"❤️ {p['hp']}/{p['max_hp']}")
col4.metric("Dano", f"🗡️ {get_player_total_atk()}")
col5.metric("Ouro", f"💰 {p['gold']}")  # <--- Ouro isolado em lugar próprio!

rar_icon = RARITY_COLORS[p['weapon_rarity']]
lvl_str = f" (+{p['weapon_level']})" if p['weapon_level'] > 0 else ""
st.caption(f"**Arma Equipada:** {rar_icon} **{p['weapon_name']}**{lvl_str} | Bônus: +{p['weapon_atk'] + (p['weapon_level']*3)} Dano")

st.divider()

tab_battle, tab_upgrades = st.tabs(["⚔️ Batalha da Onda", "🛠️ Melhorias & Cura"])

with tab_battle:
    e = st.session_state.enemy
    st.subheader(f"Inimigo Atual: {e['name']}")
    
    progress_container = st.empty()
    display_hp = max(0, e["hp"])
    hp_percent = max(0.0, float(display_hp / e["max_hp"]))
    progress_container.progress(hp_percent, text=f"HP da Galinha: {display_hp}/{e['max_hp']} | Dano: ⚔️ {e['atk']}")

    btn_container = st.empty()

    if st.session_state.is_respawning:
        btn_container.button("⏳ Galinha Derrotada! Invocando próxima...", disabled=True, use_container_width=True)
        time.sleep(DEATH_COOLDOWN)
        
        spawn_wave_chicken()
        st.session_state.is_respawning = False
        st.rerun()
    else:
        if btn_container.button("🗡️ Atacar Galinha", type="primary", use_container_width=True):
            attack(progress_container)
            st.rerun()

    # LOGICA DO AVISO FIXO POR 5 SEGUNDOS (SEM SUMIR AO ATACAR)
    if st.session_state.notice_text:
        elapsed_notice = time.time() - st.session_state.notice_time
        if elapsed_notice < 5.0:
            st.info(st.session_state.notice_text)
        else:
            st.session_state.notice_text = None

with tab_upgrades:
    st.subheader("🛠️ Melhorias & Recuperação")
    
    cost_hp = 20 + (p["max_hp"] - 30) * 2
    cost_weapon = 30 + (p["weapon_level"] * 25)
    cost_heal = 10

    col_up1, col_up2 = st.columns(2)
    
    with col_up1:
        st.write(f"**Aumentar Vida Máxima (+15 HP)**")
        st.write(f"Custo: 💰 {cost_hp} Moedas")
        if st.button("❤️ Melhorar Vida", use_container_width=True):
            if p["gold"] >= cost_hp:
                p["gold"] -= cost_hp
                p["max_hp"] += 15
                p["hp"] += 15
                st.success("Vida aumentada com sucesso!")
                st.rerun()
            else:
                st.error("Ouro insuficiente!")

    with col_up2:
        st.write(f"**Aprimorar Arma (+3 Dano)**")
        st.write(f"Custo: 💰 {cost_weapon} Moedas")
        if st.button("⚔️ Melhorar Arma", use_container_width=True):
            if p["gold"] >= cost_weapon:
                p["gold"] -= cost_weapon
                p["weapon_level"] += 1
                st.success("Sua arma ficou mais forte!")
                st.rerun()
            else:
                st.error("Ouro insuficiente!")

    st.divider()
    
    st.write(f"**💤 Curar Toda a Vida**")
    st.write(f"Custo: 💰 {cost_heal} Moedas")
    if st.button("🧪 Beber Poção de Cura", use_container_width=True):
        if p["gold"] >= cost_heal:
            p["gold"] -= cost_heal
            p["hp"] = p["max_hp"]
            st.success("Sua vida foi totalmente recuperada!")
            st.rerun()
        else:
            st.error("Ouro insuficiente!")
