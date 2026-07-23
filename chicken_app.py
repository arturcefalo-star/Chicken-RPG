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

if "new_weapon_notice" not in st.session_state:
    st.session_state.new_weapon_notice = None

# --- FUNÇÕES DO JOGO ---
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
    
    base_hp = 15 + (wave - 1) * 12
    base_atk = 2 + (wave - 1) * 2
    base_gold = 4 + (wave - 1) * 4

    hp = max(5, base_hp + random.randint(-2, 4))
    atk = max(1, base_atk + random.randint(-1, 1))
    gold = max(1, base_gold + random.randint(-1, 3))
    
    name = f"{species_info['icon']} {species_info['name']}"
    
    st.session_state.enemy = {
        "name": name,
        "hp": hp,
        "max_hp": hp,
        "atk": atk,
        "gold": gold
    }

if st.session_state.enemy is None:
    spawn_wave_chicken()

def animate_health_bar(progress_container, start_hp, end_hp, max_hp, enemy_atk):
    """Anima a barra de vida descendo gradualmente"""
    steps = 10
    start_hp = max(0, start_hp)
    end_hp = max(0, end_hp)
    
    for i in range(steps + 1):
        current_hp = start_hp - ((start_hp - end_hp) * (i / steps))
        hp_percent = max(0.0, float(current_hp / max_hp))
        progress_container.progress(
            hp_percent, 
            text=f"HP da Galinha: {int(current_hp)}/{max_hp} | Dano: ⚔️ {enemy_atk}"
        )
        time.sleep(0.03)  # Velocidade da animação da barra

def attack(progress_container):
    p = st.session_state.player
    e = st.session_state.enemy

    if not e:
        return

    st.session_state.new_weapon_notice = None

    # Cálculo do Dano
    total_atk = get_player_total_atk()
    damage_to_e = max(1, total_atk + random.randint(-1, 2))
    old_hp = e["hp"]
    e["hp"] -= damage_to_e

    # Executa a Animação da Barra caindo
    animate_health_bar(progress_container, old_hp, e["hp"], e["max_hp"], e["atk"])

    # Se a Galinha Morrer
    if e["hp"] <= 0:
        time.sleep(0.4)  # Cooldown de abate (pausa após a vida zerar)
        
        p["gold"] += e["gold"]
        st.session_state.kills_in_wave += 1
        
        # Testar Drop de Arma (40% de chance)
        if random.random() < 0.40:
            drop = generate_weapon_drop()
            rar_icon = RARITY_COLORS[drop["rarity"]]
            
            if drop["atk"] > p["weapon_atk"]:
                p["weapon_atk"] = drop["atk"]
                p["weapon_name"] = drop["name"]
                p["weapon_rarity"] = drop["rarity"]
                p["weapon_level"] = 0
                
                st.session_state.new_weapon_notice = f"🎉 **NOVA ARMA EQUIPADA!** Dropou: {rar_icon} **{drop['name']}** (+{drop['atk']} Dano Base)!"
            else:
                st.session_state.new_weapon_notice = f"📦 A galinha dropou {rar_icon} {drop['name']} (+{drop['atk']} Dano), mas sua arma atual é mais forte!"

        # Checa mudança de Onda
        target = get_wave_target(st.session_state.wave)
        if st.session_state.kills_in_wave >= target:
            st.session_state.wave += 1
            st.session_state.kills_in_wave = 0
            p["max_hp"] += 10
            p["hp"] = p["max_hp"]
            st.session_state.new_weapon_notice = f"🚨 **ONDA CONCLUÍDA!** Avançou para a **Onda {st.session_state.wave}**! Sua Vida foi restaurada."

        spawn_wave_chicken()
        return

    # Contra-Ataque da Galinha (se sobreviveu)
    damage_to_p = max(1, e["atk"] + random.randint(-1, 1))
    p["hp"] -= damage_to_p

    # Derrota do Jogador
    if p["hp"] <= 0:
        p["hp"] = p["max_hp"]
        p["gold"] = max(0, p["gold"] - 15)
        st.session_state.new_weapon_notice = "☠️ Você foi derrotado! Foi restaurado na Hospedaria (-15 moedas)."

# --- INTERFACE GRÁFICA ---
st.title("🐔 Chicken Slayer RPG")

wave_target = get_wave_target(st.session_state.wave)

# Painel Superior (Status)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Onda", f"🌊 {st.session_state.wave}")
col2.metric("Abates na Onda", f"🎯 {st.session_state.kills_in_wave}/{wave_target}")
col3.metric("Vida (HP)", f"❤️ {st.session_state.player['hp']}/{st.session_state.player['max_hp']}")
col4.metric("Dano Total", f"🗡️ {get_player_total_atk()}")

# Status da Arma Atual
p = st.session_state.player
rar_icon = RARITY_COLORS[p['weapon_rarity']]
lvl_str = f" (+{p['weapon_level']})" if p['weapon_level'] > 0 else ""
st.caption(f"**Arma Atual:** {rar_icon} **{p['weapon_name']}**{lvl_str} | Bônus: +{p['weapon_atk'] + (p['weapon_level']*3)} Dano | **Ouro:** 💰 {p['gold']}")

st.divider()

# Abas Principais
tab_battle, tab_upgrades, tab_inn = st.tabs(["⚔️ Batalha da Onda", "🛠️ Melhorias", "🏥 Hospedaria"])

with tab_battle:
    e = st.session_state.enemy
    st.subheader(f"Inimigo Atual: {e['name']}")
    
    # Renderiza o container dinâmico para a Barra de Vida
    progress_container = st.empty()
    hp_percent = max(0.0, float(e["hp"] / e["max_hp"]))
    progress_container.progress(hp_percent, text=f"HP da Galinha: {e['hp']}/{e['max_hp']} | Dano: ⚔️ {e['atk']}")

    # Botão de Atacar
    if st.button("🗡️ Atacar Galinha", type="primary", use_container_width=True):
        attack(progress_container)
        st.rerun()

    # AVISO DE DROP COM TEMPO LIMITADO (5 SEGUNDOS)
    if st.session_state.new_weapon_notice:
        notice_container = st.empty()
        notice_container.info(st.session_state.new_weapon_notice)
        time.sleep(5)  # Espera 5 segundos exibindo
        notice_container.empty()  # Apaga o aviso da tela
        st.session_state.new_weapon_notice = None

with tab_upgrades:
    st.subheader("🛠️ Melhorias de Atributos")
    
    cost_hp = 20 + (p["max_hp"] - 30) * 2
    cost_weapon = 30 + (p["weapon_level"] * 25)

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

with tab_inn:
    st.subheader("🏥 Hospedaria")
    cost_heal = 10
    if st.button(f"💤 Curar Vida Toda ({cost_heal} Moedas)", use_container_width=True):
        if p["gold"] >= cost_heal:
            p["gold"] -= cost_heal
            p["hp"] = p["max_hp"]
            st.success("Você descansou e recuperou toda a sua vida!")
            st.rerun()
        else:
            st.error("Ouro insuficiente!")
