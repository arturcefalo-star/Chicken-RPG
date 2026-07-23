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

CHICKEN_BOSSES = [
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

if "enemy" not in st.session_state:
    st.session_state.enemy = None

if "new_weapon_notice" not in st.session_state:
    st.session_state.new_weapon_notice = None

# --- FUNÇÕES DO JOGO ---
def get_player_total_atk():
    p = st.session_state.player
    return p["base_atk"] + p["weapon_atk"] + (p["weapon_level"] * 3)

def generate_weapon_drop():
    wave = st.session_state.wave
    
    roll = random.random()
    if roll < (0.08 + wave * 0.02):
        rarity = "Lendária"
        mult = 5
    elif roll < (0.25 + wave * 0.02):
        rarity = "Épica"
        mult = 3
    elif roll < (0.55 + wave * 0.02):
        rarity = "Rara"
        mult = 2
    else:
        rarity = "Comum"
        mult = 1

    base_bonus = wave * 4
    atk = random.randint(2, 5) * mult + base_bonus
    name = random.choice(WEAPON_NAMES[rarity])
    
    return {"name": name, "rarity": rarity, "atk": atk}

def spawn_wave_chicken():
    wave = st.session_state.wave
    
    # Define o boss da onda (escala infinitamente se passar dos chefes da lista)
    boss_idx = min(wave - 1, len(CHICKEN_BOSSES) - 1)
    boss_info = CHICKEN_BOSSES[boss_idx]
    
    # Atributos escalam forte a cada onda
    hp = 20 + (wave - 1) * 35
    atk = 3 + (wave - 1) * 4
    gold = 15 + (wave - 1) * 20
    
    name = f"{boss_info['icon']} {boss_info['name']} (Onda {wave})"
    
    st.session_state.enemy = {
        "name": name,
        "hp": hp,
        "max_hp": hp,
        "atk": atk,
        "gold": gold
    }

if st.session_state.enemy is None:
    spawn_wave_chicken()

def attack():
    time.sleep(0.2)  # Cooldown simples
    p = st.session_state.player
    e = st.session_state.enemy

    if not e:
        return

    # Limpa aviso anterior ao atacar novamente
    st.session_state.new_weapon_notice = None

    # Ataque do Jogador
    total_atk = get_player_total_atk()
    damage_to_e = max(1, total_atk + random.randint(-1, 2))
    e["hp"] -= damage_to_e

    # Venceu a Galinha da Onda!
    if e["hp"] <= 0:
        p["gold"] += e["gold"]
        
        # Testar Drop de Arma (70% de chance de rolar drop ao derrotar o chefe da onda)
        if random.random() < 0.70:
            drop = generate_weapon_drop()
            rar_icon = RARITY_COLORS[drop["rarity"]]
            
            # Se a arma for melhor que o dano base atual da arma
            if drop["atk"] > p["weapon_atk"]:
                p["weapon_atk"] = drop["atk"]
                p["weapon_name"] = drop["name"]
                p["weapon_rarity"] = drop["rarity"]
                p["weapon_level"] = 0  # Reseta o nível da nova arma
                
                st.session_state.new_weapon_notice = f"🎉 **NOVA ARMA EQUIPADA!** Você pegou: {rar_icon} **{drop['name']}** (+{drop['atk']} Dano Base)!"
            else:
                st.session_state.new_weapon_notice = f"📦 A galinha dropou {rar_icon} {drop['name']} (+{drop['atk']} Dano), mas sua arma atual é mais forte!"

        # Avança para a próxima onda
        st.session_state.wave += 1
        spawn_wave_chicken()
        return

    # Contra-Ataque da Galinha
    damage_to_p = max(1, e["atk"] + random.randint(-1, 1))
    p["hp"] -= damage_to_p

    # Derrota do Jogador
    if p["hp"] <= 0:
        p["hp"] = p["max_hp"]
        p["gold"] = max(0, p["gold"] - 15)
        st.session_state.new_weapon_notice = "☠️ Você perdeu a batalha! Foi restaurado na Hospedaria (-15 moedas)."

# --- INTERFACE GRÁFICA ---
st.title("🐔 Chicken Slayer RPG")

# Painel Superior (Status)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Onda", f"🌊 {st.session_state.wave}")
col2.metric("Vida (HP)", f"❤️ {st.session_state.player['hp']}/{st.session_state.player['max_hp']}")
col3.metric("Ouro", f"💰 {st.session_state.player['gold']}")
col4.metric("Dano Total", f"🗡️ {get_player_total_atk()}")

# Status da Arma Atual
p = st.session_state.player
rar_icon = RARITY_COLORS[p['weapon_rarity']]
lvl_str = f" (+{p['weapon_level']})" if p['weapon_level'] > 0 else ""
st.caption(f"**Arma Atual:** {rar_icon} **{p['weapon_name']}**{lvl_str} | Bônus: +{p['weapon_atk'] + (p['weapon_level']*3)} Dano")

st.divider()

# Abas Principais
tab_battle, tab_upgrades, tab_inn = st.tabs(["⚔️ Batalha da Onda", "🛠️ Melhorias", "🏥 Hospedaria"])

with tab_battle:
    e = st.session_state.enemy
    st.subheader(f"Galinha da Onda: {e['name']}")
    
    # Barra de Vida da Galinha
    hp_percent = max(0.0, float(e["hp"] / e["max_hp"]))
    st.progress(hp_percent, text=f"HP da Galinha: {e['hp']}/{e['max_hp']} | Dano dela: ⚔️ {e['atk']}")

    # Botão de Atacar
    if st.button("🗡️ Atacar Galinha", type="primary", use_container_width=True):
        attack()
        st.rerun()

    # AVISO LOGO ABAIXO DO BOTÃO DE ATACAR
    if st.session_state.new_weapon_notice:
        st.info(st.session_state.new_weapon_notice)

with tab_upgrades:
    st.subheader("🛠️ Melhorias de Atributos")
    
    # Custo de upgrades baseado no nível atual
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
