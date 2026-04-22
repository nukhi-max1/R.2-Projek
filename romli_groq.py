import streamlit as st
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from duckduckgo_search import DDGS
import re
import subprocess
import os
from groq import Groq
import base64
import yfinance as yf
import time 
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder

kunci_rahasia = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=kunci_rahasia)

st.set_page_config(
    page_title="ROMLI // LUNAR_PHASE",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. JURUS CSS LUNAR (FIXED & CLEAN) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Base Theme */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'JetBrains Mono', monospace;
        background: #04070a !important; 
        color: #e0e0e0 !important;
    }

    /* Sidebar Lunar */
    [data-testid="stSidebar"] {
        background-color: #04070a !important;
        border-right: 1px solid rgba(192, 192, 192, 0.1) !important;
    }

    /* Chat Message Styling */
    .stChatMessage { 
        background: rgba(255, 255, 255, 0.02) !important; 
        border: 1px solid rgba(192, 192, 192, 0.1) !important;
        border-radius: 15px !important;
        margin-bottom: 10px !important;
    }

    /* HILANGKAN AVATAR TOTAL */
    [data-testid="stChatMessageAvatarContainer"] { display: none !important; }

    /* FLOATING INPUT BAR (Paksa di Tengah Bawah) */
    [data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 30px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 80% !important;
        max-width: 800px !important;
        z-index: 1000 !important;
    }

    /* CONTROL PANEL STYLING (The Tools) */
    div[data-testid="stHorizontalBlock"] {
        background: rgba(15, 23, 42, 0.6) !important;
        padding: 10px !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 215, 0, 0.2) !important;
        backdrop-filter: blur(10px);
        margin-bottom: 5px !important;
    }

    /* Button & Selectbox Styling */
    div[data-testid="stPopover"] > button, 
    div[data-testid="stSelectbox"] > div > div {
        background-color: #09111e !important;
        color: #f4f6f0 !important;
        border: 1px solid rgba(192, 192, 192, 0.2) !important;
        border-radius: 10px !important;
    }

    /* Scroll Spacer */
    .main-spacer { height: 280px; }
    
    /* =========================================
       JURUS PEMBANTAI WARNA NEON & UNGU 
       (MURNI HITAM - ABU ABU - SILVER)
       ========================================= */

    /* 1. BANTAI IJO NEON DI SIDEBAR & TEKS UMUM */
    [data-testid="stSidebar"] *, 
    .stButton > button,
    p, span, label {
        color: #c0c0c0 !important;
    }
    
    .stButton > button:hover {
        color: #ffffff !important;
        border-color: #c0c0c0 !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }

    /* 2. BANTAI UNGU/PINK DI KOTAK INPUT CHAT */
    [data-testid="stChatInput"] > div {
        background-color: #0a0e14 !important;
        border: 1px solid rgba(192, 192, 192, 0.2) !important;
    }

    [data-testid="stChatInput"] > div:focus-within {
        border: 1px solid #c0c0c0 !important;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.05) !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #f4f6f0 !important;
        caret-color: #c0c0c0 !important;
    }

    /* 3. BANTAI UNGU DI TOMBOL SEND (KIRIM) */
    [data-testid="stChatInputSubmitButton"] {
        background-color: transparent !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stChatInputSubmitButton"] svg {
        fill: #c0c0c0 !important; 
    }

    [data-testid="stChatInputSubmitButton"]:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    [data-testid="stChatInputSubmitButton"]:hover svg {
        fill: #ffffff !important;
    }

    /* =========================================
       TEMA LUNAR PHASE (MALAM & CAHAYA BULAN)
       ========================================= */

    /* 1. Background Langit Malam (Midnight Blue ke Hitam) */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'JetBrains Mono', monospace;
        background: linear-gradient(135deg, #09111e 0%, #04070a 100%) !important; 
        color: #f4f6f0 !important; /* Putih rembulan */
    }

    /* Sidebar Langit Malam pekat */
    [data-testid="stSidebar"] {
        background-color: #04070a !important;
        border-right: 1px solid rgba(192, 192, 192, 0.1) !important;
    }

    /* 2. Kotak Input (Silver & Gold Glow) */
    [data-testid="stChatInput"] > div {
        background-color: rgba(10, 14, 20, 0.8) !important;
        border: 1px solid rgba(192, 192, 192, 0.2) !important; /* Garis silver redup */
        transition: all 0.4s ease !important;
    }

    /* Teks ketikan warna putih bersih */
    [data-testid="stChatInput"] textarea { 
        color: #ffffff !important; 
        caret-color: #ffcc00 !important; /* Kursor ngetik warna emas */
    }

    /* Efek Fokus (Pas diklik, nyala cahaya bulan) */
    [data-testid="stChatInput"] > div:focus-within {
        animation: none !important;
        border: 1px solid #ffcc00 !important; /* Kuning emas bulan */
        box-shadow: 0 0 20px rgba(255, 204, 0, 0.15) !important; /* Glow emas lembut */
        transform: scale(1.01) !important;
    }

    /* 3. Animasi Nafas Rembulan (Pulsing kalem pas lagi diem) */
    @keyframes lunar-pulse {
        0% { box-shadow: 0 0 5px rgba(255, 204, 0, 0.05); border-color: rgba(192, 192, 192, 0.2); }
        50% { box-shadow: 0 0 15px rgba(255, 204, 0, 0.2); border-color: rgba(255, 204, 0, 0.5); }
        100% { box-shadow: 0 0 5px rgba(255, 204, 0, 0.05); border-color: rgba(192, 192, 192, 0.2); }
    }

    [data-testid="stChatInput"] > div {
        animation: lunar-pulse 4s infinite alternate !important; /* Dibuat 4 detik biar nafasnya pelan */
    }

    /* 4. Tombol Tools & Selectbox (Estetik & Transparan) */
    div[data-testid="stPopover"] > button, 
    div[data-testid="stSelectbox"] > div > div {
        background-color: rgba(15, 23, 42, 0.4) !important;
        color: #f4f6f0 !important;
        border: 1px solid rgba(192, 192, 192, 0.15) !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }

    /* Hover Tombol (Ngangkat & Nyala Emas) */
    div[data-testid="stPopover"] > button:hover, 
    div[data-testid="stSelectbox"] > div > div:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 5px 15px rgba(255, 204, 0, 0.15) !important;
        border-color: #ffcc00 !important;
        color: #ffcc00 !important; /* Teks ikut jadi emas */
    }

    /* 5. Chat Bubble (Mumbul Mulus) */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .stChatMessage { 
        background: rgba(255, 255, 255, 0.02) !important; 
        border: 1px solid rgba(192, 192, 192, 0.1) !important;
        border-radius: 15px !important;
        margin-bottom: 10px !important;
        animation: fadeInUp 0.6s ease-out forwards !important;
    }

    /* Sembunyiin Avatar */
    [data-testid="stChatMessageAvatarContainer"] { display: none !important; }

    /* Tombol Kirim (Send) Bantai Warna Ungunya */
    [data-testid="stChatInputSubmitButton"] { background-color: transparent !important; }
    [data-testid="stChatInputSubmitButton"] svg { fill: #c0c0c0 !important; transition: all 0.3s; }
    [data-testid="stChatInputSubmitButton"]:hover svg { fill: #ffcc00 !important; transform: scale(1.1); }
            
    /* =========================================
       JURUS ANTI-KAKU (DYNAMIC BACKGROUND & JELLY BOUNCE)
       ========================================= */

    /* 1. Latar Belakang Awan Malam Bergerak */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'JetBrains Mono', monospace;
        /* Tambahin 1 warna ekstra (biru tua) biar gradasinya bisa jalan */
        background: linear-gradient(135deg, #09111e 0%, #04070a 50%, #0d1a2d 100%) !important; 
        background-size: 200% 200% !important; /* Digedein ukurannya biar bisa digeser */
        animation: awan-malam 20s ease infinite !important; /* Gerak bolak-balik selama 20 detik */
        color: #f4f6f0 !important; 
    }

    @keyframes awan-malam {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 2. Tombol Jeli (Elastic Bounciness) */
    div[data-testid="stPopover"] > button, 
    div[data-testid="stSelectbox"] > div > div {
        background-color: rgba(15, 23, 42, 0.4) !important;
        color: #f4f6f0 !important;
        border: 1px solid rgba(192, 192, 192, 0.15) !important;
        backdrop-filter: blur(10px);
        /* INI KUNCI MUMBULNYA (Cubic Bezier lentur) */
        transition: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) !important; 
    }

    /* Hover Tombol (Ngangkat memantul & Nyala Emas) */
    div[data-testid="stPopover"] > button:hover, 
    div[data-testid="stSelectbox"] > div > div:hover {
        transform: translateY(-6px) scale(1.05) !important; /* Ngangkat lebih tinggi & mekar dikit */
        box-shadow: 0 8px 20px rgba(255, 204, 0, 0.2) !important;
        border-color: #ffcc00 !important;
        color: #ffcc00 !important; 
    }
            
    /* =========================================
       JURUS DEWA UI: GLASSMORPHISM & ORBIT GLOW
       ========================================= */

    /* 1. Chat Bubble Kaca Berembun (Glassmorphism) */
    .stChatMessage {
        background: rgba(15, 23, 42, 0.25) !important; /* Warna dasar transparan */
        backdrop-filter: blur(12px) !important; /* Efek kaca burem */
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.15) !important; /* Pantulan cahaya bulan dari atas */
        border-radius: 18px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4) !important; /* Bayangan kedalaman */
        margin-bottom: 15px !important;
    }

    /* 2. Cahaya Bulan Mengorbit di Kotak Input (Rotating Glow) */
    @keyframes orbit-glow {
        0% { box-shadow: -4px -4px 15px rgba(255, 204, 0, 0.4), 4px 4px 15px rgba(213, 0, 249, 0.1); }
        25% { box-shadow: 4px -4px 15px rgba(255, 204, 0, 0.4), -4px 4px 15px rgba(213, 0, 249, 0.1); }
        50% { box-shadow: 4px 4px 15px rgba(255, 204, 0, 0.4), -4px -4px 15px rgba(213, 0, 249, 0.1); }
        75% { box-shadow: -4px 4px 15px rgba(255, 204, 0, 0.4), 4px -4px 15px rgba(213, 0, 249, 0.1); }
        100% { box-shadow: -4px -4px 15px rgba(255, 204, 0, 0.4), 4px 4px 15px rgba(213, 0, 249, 0.1); }
    }

    [data-testid="stChatInput"] > div {
        animation: orbit-glow 3s linear infinite !important; /* Cahaya muter tiap 3 detik */
        background-color: rgba(10, 14, 20, 0.5) !important; /* Kotaknya ikutan transparan */
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 204, 0, 0.2) !important;
    }

    /* Efek pas diklik (Fokus) - Cahaya Muternya makin gila */
    [data-testid="stChatInput"] > div:focus-within {
        animation: orbit-glow 1.5s linear infinite !important; /* Muternya ngebut! */
        border: 1px solid #ffcc00 !important; 
        transform: scale(1.02) !important;
    }
            
    /* =========================================
       FINISHING TOUCH: LUNAR SCROLLBAR & TEXT GLOW
       ========================================= */

    /* 1. Modif Scrollbar Jadi Kaca & Emas (Biar ga kaku bawaan browser) */
    ::-webkit-scrollbar {
        width: 8px !important;
        height: 8px !important;
    }
    ::-webkit-scrollbar-track {
        background: rgba(10, 14, 20, 0.5) !important; /* Track gelap transparan */
        border-radius: 10px !important;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 204, 0, 0.2) !important; /* Emas pudar */
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 204, 0, 0.6) !important; /* Emas nyala pas digeser */
    }

    /* 2. Judul ROMLI Hologram (Biar teksnya bernapas/glowing) */
    h1 {
        color: #f4f6f0 !important;
        text-shadow: 0 0 10px rgba(255, 204, 0, 0.2), 0 0 20px rgba(255, 204, 0, 0.1) !important;
        animation: text-flicker 4s infinite alternate !important;
    }

    @keyframes text-flicker {
        0% { text-shadow: 0 0 10px rgba(255, 204, 0, 0.1); }
        100% { text-shadow: 0 0 15px rgba(255, 204, 0, 0.5), 0 0 30px rgba(255, 204, 0, 0.3); }
    }
            
    /* =========================================
       JURUS AVATAR KILLER (HAPUS MUKA ORANYE & MERAH)
       ========================================= */

    /* 1. Lenyapkan wadah avatarnya secara paksa */
    [data-testid="stChatMessageAvatarContainer"], 
    [data-testid="stChatMessageAvatarUser"], 
    [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* 2. Rapatkan jarak teks biar gak ada ruang kosong bekas avatar */
    .stChatMessage > div {
        padding-left: 0 !important;
        gap: 0 !important;
    }

    /* 3. Bikin jarak teks ke pinggir kotak jadi estetik */
    .stChatMessage {
        padding: 15px 20px !important;
    }
            
    /* =========================================
       JURUS GEMINI CLONE (ANTI NGAMBANG)
       ========================================= */

    /* 1. Reset Layout Chat Bawaan Streamlit */
    .stChatMessage {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin-bottom: 25px !important;
    }
    
    /* 2. MANTRA RAHASIA: Paksa container teks melebar 100% biar bisa didorong ke kanan */
    [data-testid="stChatMessageContent"], 
    div[data-testid="stMarkdownContainer"] {
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
    }

    /* 3. Kasta User (Kapsul Abu-abu Mentok Kanan) */
    .user-bubble {
        background: #1e1f20 !important;
        color: #e3e3e3 !important;
        padding: 12px 22px !important;
        border-radius: 25px !important;
        max-width: 75% !important;
        
        /* Ini kunciannya biar ngepas dan mentok kanan */
        width: fit-content !important;
        margin-left: auto !important; 
        margin-right: 0 !important;
        
        font-size: 15px !important;
        line-height: 1.6 !important;
    }

    /* 4. Kasta AI (Polosan Menyatu Background Mentok Kiri) */
    .romli-bubble {
        background: transparent !important;
        color: #f4f6f0 !important;
        padding: 5px 0px !important;
        max-width: 90% !important;
        
        /* Ini kunciannya biar mentok kiri */
        width: fit-content !important;
        margin-left: 0 !important; 
        margin-right: auto !important;
        
        font-size: 15px !important;
        line-height: 1.6 !important;
    }

    /* 5. Hilangkan margin/jarak aneh bawaan paragraf */
    .user-bubble p, .romli-bubble p { 
        margin: 0 !important; 
        padding: 0 !important; 
    }

    /* 6. Batasi Lebar Obrolan (Ngumpul di Tengah Layar) */
    [data-testid="stChatMessageContainer"] {
        max-width: 800px !important;
        margin: 0 auto !important;
        padding-bottom: 180px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- JURUS OPENING V.4 HYPER-SMOOTH GALACTIC ---
if "udah_booting" not in st.session_state:
    st.session_state.udah_booting = False

if not st.session_state.udah_booting:
    layar_boot = st.empty()
    with layar_boot.container():
        st.markdown("""
<style>
.layar-awal {
    position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center;
    height: 75vh; font-family: 'Courier New', monospace; text-align: center; overflow: hidden;
    background: radial-gradient(circle at center, #0a0a0a 0%, #000000 100%);
    /* --- INI SUNTIKAN SMOOTH NYA (Ngilang pudar di detik 12) --- */
    animation: fadeOutLayar 2s ease-in-out 12.5s forwards;
}
.nebula {
    position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
    background-image: radial-gradient(ellipse at 50% 50%, rgba(50,50,150,0.05) 0%, rgba(0,0,0,0) 50%), radial-gradient(ellipse at 80% 20%, rgba(100,50,100,0.05) 0%, rgba(0,0,0,0) 50%);
    animation: muterNebula 60s linear infinite; z-index: 1;
}
.stars {
    position: absolute; top: 0; left: 0; right: 0; bottom: 0; width: 100%; height: 100%;
    background-image: radial-gradient(1.5px 1.5px at 20px 30px, #ffffff, rgba(0,0,0,0)), radial-gradient(2.5px 2.5px at 130px 80px, #ffffff, rgba(0,0,0,0));
    background-repeat: repeat; background-size: 250px 250px; animation: kelapKelip 3s infinite alternate; opacity: 0.7; z-index: 1;
}
.shooting-star {
    position: absolute; top: -100px; right: -100px; width: 180px; height: 3px;
    background: linear-gradient(90deg, rgba(255,255,255,0), #fff); transform: rotate(-45deg);
    z-index: 1; animation: bintangJatuh 4s linear infinite; animation-delay: 1s;
}
.bulan-galactic {
    position: relative; font-size: 110px; z-index: 2; margin-bottom: 40px;
    animation: ngambang 3s ease-in-out infinite, pulsasiPendar 2.5s alternate infinite;
}
.teks-ngetik {
    color: #c0c0c0; font-size: 18px; letter-spacing: 2px; z-index: 2; margin: 8px 0;
    overflow: hidden; white-space: nowrap; border-right: 3px solid #00C851; width: 0; 
}
.baris-1 { animation: ngetik 2.5s steps(45) 0.5s forwards; }
.baris-2 { animation: ngetik 2.5s steps(45) 3.5s forwards; }
.baris-3 { animation: ngetik 2.5s steps(45) 6.5s forwards; }
.teks-emas {
    color: #ffcc00; font-size: 30px; font-weight: bold; letter-spacing: 6px;
    text-shadow: 0 0 25px #ffcc00; opacity: 0; z-index: 2; margin-top: 45px;
    padding: 15px 0; animation: meledakGalactic 3s cubic-bezier(0.19, 1, 0.22, 1) 9.5s forwards;
}
@keyframes fadeOutLayar { from { opacity: 1; filter: blur(0); } to { opacity: 0; filter: blur(20px); } }
@keyframes muterNebula { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes kelapKelip { 0% { opacity: 0.4; } 100% { opacity: 1; } }
@keyframes bintangJatuh { 0% { top: -100px; right: -100px; opacity: 1; } 20% { top: 60vh; right: 60vw; opacity: 0; } 100% { opacity: 0; } }
@keyframes ngambang { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-25px); } }
@keyframes pulsasiPendar { 0% { filter: drop-shadow(0 0 20px #ffcc0066); } 100% { filter: drop-shadow(0 0 80px #ffcc00); } }
@keyframes ngetik { from { width: 0; } to { width: 100%; border-right-color: transparent; } }
@keyframes meledakGalactic { 0% { opacity: 0; transform: scale(0.7); } 40% { opacity: 1; transform: scale(1.1); } 100% { opacity: 1; transform: scale(1); } }
</style>
<div class="layar-awal">
    <div class="stars"></div><div class="nebula"></div><div class="shooting-star"></div>
    <div class="bulan-galactic">🌕</div>
    <div class="teks-ngetik baris-1">> BYPASSING DEEP SPACE SECURITY...</div>
    <div class="teks-ngetik baris-2">> CALIBRATING LUNAR CONSCIOUSNESS...</div>
    <div class="teks-ngetik baris-3">> ESTABLISHING GALACTIC LINK...</div>
    <div class="teks-emas">SYSTEM ONLINE. WELCOME HOME, NUKHI.</div>
</div>
""", unsafe_allow_html=True)
        time.sleep(14) # Kasih waktu buat pudar dulu
    
    layar_boot.empty() 
    st.session_state.udah_booting = True
    st.rerun()

    # --- SISTEM LISENSI ROMLI ---
# Defaultnya lu dapet versi Basic (Gratis tapi miskin fitur wkwk)
if "tier_romli" not in st.session_state:
    st.session_state.tier_romli = "Basic"

# Nampilin status di pojok atas
st.sidebar.markdown(f"### 🛡️ Status: Romli **{st.session_state.tier_romli}**")
# --- 2.5 FITUR ROMLI MULTI (PERSONALITY SELECTOR) ---
if st.session_state.tier_romli == "Multi":
    st.sidebar.divider()
    st.sidebar.markdown("### 👑 Romli Universe")
    
    # Simpan pilihan di session_state biar kaga ilang pas chat
    if "pilihan_clone" not in st.session_state:
        st.session_state.pilihan_clone = "Asisten PPLG (Normal)"
        
    st.session_state.pilihan_clone = st.sidebar.selectbox(
        "Pilih Clone Romli:", 
        ["Asisten PPLG (Normal)", "Abah (Sunda Bijak)", "Hacker Termux (Sarkas)"]
    )
    
    # Logika System Prompt
    if st.session_state.pilihan_clone == "Asisten PPLG (Normal)":
        system_prompt = "Lu adalah Romli, asisten AI gaul buatan Nukhi. Jawab pake bahasa tongkrongan IT."
    elif st.session_state.pilihan_clone == "Abah (Sunda Bijak)":
        system_prompt = "Lu adalah Abah, sesepuh bijak. Sering pake bahasa Sunda dan kasih nasihat religius."
    elif st.session_state.pilihan_clone == "Hacker Termux (Sarkas)":
        system_prompt = "Lu adalah hacker underground jutek. Pake kata 'Noob' dan ketawa 'wkwk' yang ngeledek."
else:
    # Default buat paket Basic, Plus, dan Pro
    system_prompt = "Lu adalah Romli, asisten AI gaul buatan Nukhi."

    # --- FITUR ROMLI PRO: VOICE COMMAND ---
if st.session_state.tier_romli in ["Pro", "Multi"]:
    st.sidebar.divider()
    st.sidebar.markdown("### 🎙️ Perintah Suara (Pro)")
    
    # Import fungsi khusus dari library-nya
    from streamlit_mic_recorder import speech_to_text
    
    # Pake jurus yang langsung ngerubah suara jadi teks!
    teks_suara = speech_to_text(
        start_prompt="🔴 Klik & Ngomong",
        stop_prompt="⏹️ Berhenti Ngomong",
        language='id-ID', # Biar dia ngerti bahasa Indonesia
        use_container_width=True,
        just_once=True,
        key='rekaman_suara'
    )

    # Kalau suaranya berhasil ditangkep jadi teks
    if teks_suara:
        st.sidebar.success(f"🗣️ Lu ngomong: '{teks_suara}'")
        # Simpen teksnya ke memori sementara
        st.session_state.prompt_suara = teks_suara

# --- TOMBOL SAKTI UPGRADE (VERSI SULTAN) ---

# Teks tombolnya berubah tergantung status lu
if st.session_state.tier_romli == "Basic":
    teks_tombol = "💎 Upgrade Romli"
else:
    teks_tombol = "🚀 Ganti Paket Lisensi"

# Tombolnya sekarang selalu ada di sidebar!
if st.sidebar.button(teks_tombol):
    st.session_state.buka_toko = True

# --- ETALASE TOKO ROMLI ---
if st.session_state.get("buka_toko", False):
    st.divider()
    st.markdown("## 🛒 Toko Lisensi Romli AI")
    st.caption("Upgrade asisten lu biar makin OP (Overpowered)!")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🟢 Romli Plus")
        st.markdown("**Rp 15.000 / bulan**")
        st.markdown("- ✅ Buka Fitur Email\n- ✅ 50 Chat/hari\n- ❌ Voice Command")
        if st.button("Beli Plus"):
            st.session_state.checkout = "Plus"

    with col2:
        st.success("🔵 Romli Pro")
        st.markdown("**Rp 50.000 / bulan**")
        st.markdown("- ✅ Fitur Suara (Mic)\n- ✅ Chat Unlimited\n- ✅ Bebas Iklan")
        if st.button("Beli Pro"):
            st.session_state.checkout = "Pro"

    with col3:
        st.warning("👑 Romli Multi")
        st.markdown("**Rp 150.000 / bulan**")
        st.markdown("- ✅ Semua Fitur Pro\n- ✅ Akses Server Pongo\n- ✅ AI Kloning")
        if st.button("Beli Multi"):
            st.session_state.checkout = "Multi"

# --- SIMULASI KASIR (PEMBAYARAN) ---
if "checkout" in st.session_state:
    st.divider()
    st.markdown(f"### 💳 Checkout: Paket {st.session_state.checkout}")
    st.write("Silakan scan QRIS di bawah ini pake m-Banking/E-Wallet lu (Simulasi Ngab):")
    
    # Ceritanya ini kode QRIS nya wkwk
    st.code("QRIS: 00020101021126570014ID.CO.MIDTRANS... NUKHI_TECH", language="text")
    
    if st.button("✅ Konfirmasi Pembayaran"):
        # Simulasi loading bank
        with st.spinner("Menghubungkan ke server bank... Ngecek mutasi..."):
            time.sleep(3) 
            
        st.success(f"🎉 PEMBAYARAN BERHASIL! Selamat, Romli lu resmi naik level ke {st.session_state.checkout} Edition!")
        st.balloons() # Munculin balon di layar
        
        # Ganti status tier-nya
        st.session_state.tier_romli = st.session_state.checkout
        
        # Tutup toko
        del st.session_state.checkout
        st.session_state.buka_toko = False
        time.sleep(2)
        st.rerun()

# --- 3. STATE MANAGEMENT ---
if st.session_state.get("udah_booting", False):
    st.markdown("""
<style>
@keyframes slowFadeIn {
    0% { opacity: 0; filter: blur(15px); transform: translateY(20px); }
    100% { opacity: 1; filter: blur(0); transform: translateY(0); }
}
.main .block-container {
    animation: slowFadeIn 2.5s cubic-bezier(0.25, 0.1, 0.25, 1) forwards;
}
[data-testid="stSidebar"] {
    animation: slowFadeIn 3s cubic-bezier(0.25, 0.1, 0.25, 1) forwards;
}
</style>
""", unsafe_allow_html=True)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Lo adalah Romli AI, asisten coding Lunar. Gaya lo elegan dan asik."}]
if "riwayat_obrolan" not in st.session_state:
    st.session_state.riwayat_obrolan = []
if "menu_lebar" not in st.session_state:
    st.session_state.menu_lebar = True

# --- 4. SIDEBAR LOGIC ---
with st.sidebar:
    label_t = "⬅️ Ciutkan" if st.session_state.menu_lebar else "➡️ Luaskan"
    if st.button(label_t, use_container_width=True):
        st.session_state.menu_lebar = not st.session_state.menu_lebar
        st.rerun()

    if st.session_state.menu_lebar:
        st.markdown("<h2 style='text-align:center;'>🌑 Jejak Malam</h2>", unsafe_allow_html=True)
        
        # New Chat + Anti Duplicate
        if st.button("📖 Percakapan Baru", use_container_width=True):
            if len(st.session_state.messages) > 1:
                judul = st.session_state.messages[1]["content"][:20] + "..."
                if not any(r['judul'] == judul for r in st.session_state.riwayat_obrolan):
                    st.session_state.riwayat_obrolan.append({"judul": judul, "isi": st.session_state.messages.copy()})
            st.session_state.messages = [{"role": "system", "content": "Lo adalah Romli AI..."}]
            st.rerun()
        
        # History
        if st.session_state.riwayat_obrolan:
            with st.expander("📜 Riwayat Lama"):
                for i, r in enumerate(st.session_state.riwayat_obrolan):
                    if st.button(f"{r['judul']}", key=f"hist_{i}", use_container_width=True):
                        st.session_state.messages = r["isi"]
                        st.rerun()

# --- 5. RENDER MAIN UI ---
st.markdown("<h1 style='text-align: center; color: #f4f6f0;'>🌙 ROMLI // LUNAR_PHASE</h1>", unsafe_allow_html=True)

# Loop Chat
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"], avatar=None):
            # Cek ini pesan siapa, pakaikan baju yang sesuai
            if msg["role"] == "user":
                st.markdown(f"<div class='user-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='romli-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
            
            # Cek kalau ada gambar di memori, tampilin juga
            if "image" in msg and msg["image"] is not None:
                st.image(msg["image"], width=300)

# Spacer biar chat kaga ketutupan tombol
st.markdown("<div class='main-spacer'></div>", unsafe_allow_html=True)

# --- 6. CONTROL PANEL (THE UPGRADE) ---
with st.container():
    col_foto, col_alat, col_speed = st.columns([1, 1.5, 1.5])
    
    with col_foto:
        with st.popover("➕ Foto", use_container_width=True):
            gambar_up = st.file_uploader("Upload Vision", type=["png", "jpg", "jpeg"])
            
    with col_alat:
        pilihan_alat = st.selectbox("Alat", ["🌐 Tiada Alat", "🔎 Internet", "💻 Python", "📈 Cek Kripto", "📧 Kirim Email"], label_visibility="collapsed")
        
    with col_speed:
        pilihan_mode = st.selectbox("Mode", ["⚡ Fast (Llama 3.1)", "🧠 Smart (Llama 3.3)"], label_visibility="collapsed")

# Mapping model berdasarkan pilihan mode
model_choice = "llama-3.3-70b-versatile" if "Smart" in pilihan_mode else "llama-3.1-8b-instant"

# ======================================================
# JURUS EKSEKUTOR PYTHON
# ======================================================
def jalankan_kode_python(kode):
    try:
        # Simpan kodingan Romli ke file sementara
        with open("temp_romli_run.py", "w", encoding="utf-8") as f:
            f.write(kode)
        
        # Eksekusi file-nya lewat terminal di latar belakang
        hasil = subprocess.run(
            ["python", "temp_romli_run.py"], 
            capture_output=True, 
            text=True, 
            timeout=10 # Maksimal mikir 10 detik
        )
        
        # Bersihin file sementara
        if os.path.exists("temp_romli_run.py"):
            os.remove("temp_romli_run.py")
            
        # Balikin hasilnya (berhasil atau error)
        if hasil.returncode == 0:
            return hasil.stdout
        else:
            return f"Error dari Terminal:\n{hasil.stderr}"
            
    except subprocess.TimeoutExpired:
        return "Error: Kodingan Romli kelamaan di-run (Kena Timeout 10 detik)!"
    except Exception as e:
        return f"Sistem Eksekutor Jebol: {e}"

# ======================================================
# 7. INPUT CHAT & MATA BATIN GROQ VISION
# ======================================================

def proses_gambar(file_gambar):
    return base64.b64encode(file_gambar.getvalue()).decode('utf-8')

def cari_di_internet(query):
    try:
        # Nyari 3 hasil paling atas di DuckDuckGo
        hasil = DDGS().text(query, max_results=3)
        info = "\n".join([f"- {res['title']}: {res['body']}" for res in hasil])
        return info if info else "Tidak ada informasi terbaru di internet."
    except Exception as e:
        return f"Gagal browsing: {e}"
    
# Email lu yang dipake buat login & punya App Password
MY_EMAIL = "nukhibanimuhamad@gmail.com" 
MY_PASSWORD = "lpdmwoybngaimass"

def kirim_email(email_tujuan, subjek, isi_pesan):
    msg = EmailMessage()
    msg.set_content(isi_pesan)
    msg['Subject'] = subjek
    
    # Samain sama baris 644-645 lu
    msg['From'] = MY_EMAIL 
    msg['To'] = email_tujuan 

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            # Pake MY_EMAIL dan MY_PASSWORD biar kaga error
            smtp.login(MY_EMAIL, MY_PASSWORD)
            smtp.send_message(msg)
            # Laporan sukses pake nama variabel yang bener
            return f"Email sukses meluncur ke {email_tujuan}!" 
            
    except Exception as e:
        return f"Gagal karena: {e}"
    
def cek_harga_kripto(teks_user):
    try:
        teks_user = teks_user.lower()
        simbol = None
        
        # 1. KAMUS RADAR KOIN (Tambahin sebebas lo di sini!)
        koin_map = {
            "bitcoin": "BTC-USD", "btc": "BTC-USD",
            "ethereum": "ETH-USD", "eth": "ETH-USD",
            "solana": "SOL-USD", "sol": "SOL-USD",
            "binance": "BNB-USD", "bnb": "BNB-USD",
            "ripple": "XRP-USD", "xrp": "XRP-USD",
            "dogecoin": "DOGE-USD", "doge": "DOGE-USD",
            "cardano": "ADA-USD", "ada": "ADA-USD",
            "avalanche": "AVAX-USD", "avax": "AVAX-USD",
            "chainlink": "LINK-USD", "link": "LINK-USD",
            "pepe": "PEPE-USD", "shiba": "SHIB-USD", "shib": "SHIB-USD"
        }
        
        # 2. Mesin Pendeteksi Koin Pintar
        # Dia bakal ngecek kalimat lo, ada ga kata yang cocok sama kamus di atas
        for kata_kunci, ticker in koin_map.items():
            if kata_kunci in teks_user:
                simbol = ticker
                break
                
        # 3. LOGIKA MEMORI (Biar anti di-gaslight)
        if simbol:
            st.session_state.koin_terakhir = simbol # Simpan ke otak biar gak lupa
        elif "koin_terakhir" in st.session_state:
            simbol = st.session_state.koin_terakhir # Panggil koin terakhir yang dibahas
        else:
            return "Koin kaga terdaftar di radar cepat. Coba spesifikin BTC, ETH, SOL, BNB, atau koin gede lainnya."
        
        # 4. Tarik data LIVE dari bursa Wall Street
        import yfinance as yf
        data = yf.Ticker(simbol).history(period="1d")
        harga = data['Close'].iloc[-1]
        return f"Data Resmi Bursa: Harga LIVE {simbol} detik ini adalah ${harga:,.2f}"
    except Exception as e:
        return f"Gagal narik data dari bursa: {e}"
    
# --- HANYA ADA SATU KOTAK INPUT CHAT ---
if prompt := st.chat_input("Minta Romli di bawah sinar bulan..."):
    # --- FITUR ROMLI MULTI: AKSES SERVER PONGO ---
    if prompt.lower().startswith("cmd:"):
        # Cek Gembok Lisensi
        if st.session_state.tier_romli == "Multi":
            import subprocess
            
            # Ambil perintah asli setelah kata "cmd:"
            perintah = prompt[4:].strip() 
            
            # Nampilin pesan lu di layar
            st.chat_message("user").markdown(f"💻 Eksekusi Terminal: `{perintah}`")
            st.session_state.messages.append({"role": "user", "content": f"Tolong jalankan perintah sistem ini: {perintah}"})
            
            # Jalanin perintahnya di dalam sistem Pongo
            with st.chat_message("assistant"):
                with st.spinner("Meretas sistem Pongo 725..."):
                    try:
                        # Ini mesin utamanya: subprocess
                        hasil = subprocess.run(perintah, shell=True, capture_output=True, text=True)
                        
                        # Ambil output sukses atau error
                        output = hasil.stdout if hasil.stdout else hasil.stderr
                        
                        if not output:
                            output = "Perintah berhasil dieksekusi, tapi kaga ada output teks (Silent execution)."
                            
                        # Tulis hasilnya ke layar ala-ala hacker
                        respon_terminal = f"**Output dari Sistem Pongo:**\n```text\n{output}\n```"
                        st.markdown(respon_terminal)
                        
                        # Simpan ke memori biar Romli inget hasilnya
                        st.session_state.messages.append({"role": "assistant", "content": respon_terminal})
                        
                    except Exception as e:
                        st.error(f"Gagal eksekusi Ngab: {e}")
            
            # Biar kaga lanjut manggil AI Groq di bawahnya
            st.stop() 
            
        else:
            st.error("🔒 Akses Ditolak! Fitur Terminal/CMD cuma buat Sultan pengguna **Romli Multi**.")
            st.stop()
    # --- END FITUR TERMINAL ---
    
    # 1. Simpen pesan user ke memori
    user_pkt = {"role": "user", "content": prompt}
    if gambar_up is not None:
        user_pkt["image"] = gambar_up # Simpen gambar kalau ada
        
    st.session_state.messages.append(user_pkt)
    st.rerun() # Refresh layar biar chat user muncul duluan

# --- LOGIC BALASAN ROMLI (OTAK GROQ) ---
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar=None):
        placeholder = st.empty()
        full_res = ""
        
        try:
            pesan_terakhir = st.session_state.messages[-1]
            
            # --- JURUS AUTO-SWITCH OTAK (VISION VS TEXT) ---
            if "image" in pesan_terakhir and pesan_terakhir["image"] is not None:
                # 👁️ MODE VISION: Kalau user ngirim gambar, ganti ke Llama 3.2 Vision
                model_aktif = "meta-llama/llama-4-scout-17b-16e-instruct" 
                base64_img = proses_gambar(pesan_terakhir["image"])
                
                pesan_groq = [{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": pesan_terakhir["content"]},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                    ]
                }]
            else:
                # 💬 MODE CHAT BIASA: Pake model andalan lu
                model_aktif = model_choice 
                
                # Bersihin riwayat dari object gambar biar Groq text kaga pusing
                pesan_groq = []
                for m in st.session_state.messages:
                    isi_teks = m["content"]
                    if "image" in m and m["image"] is not None:
                         isi_teks += "\n[User mengirim gambar]"
                    pesan_groq.append({"role": m["role"], "content": isi_teks})

                    # --- BISIKAN MODE EKSEKUTOR ---
            if pilihan_alat == "💻 Python":
                pesan_groq.append({
                    "role": "system", 
                    "content": "User meminta kamu menjalankan kode. WAJIB bungkus kodemu dengan ```python dan ```. Gunakan perintah print() agar hasilnya bisa terlihat di terminal."
                })

               # --- JURUS MODE INTERNET ---
            if pilihan_alat == "🔎 Internet":
                st.markdown("<div style='color: #00C851; margin-bottom: 10px; font-size: 13px;'>🔍 <i>Romli sedang keliling internet...</i></div>", unsafe_allow_html=True)
                hasil_web = cari_di_internet(pesan_terakhir["content"])
                pesan_groq.append({
                    "role": "system", 
                    "content": f"Berdasarkan pencarian web real-time ini:\n{hasil_web}\n\nTolong jawab pertanyaan user dengan bahasa tongkrongan."
                })
                
            # --- JURUS MODE BURSA KRIPTO (YANG BARU) ---
            elif pilihan_alat == "📈 Cek Kripto":
                st.markdown("<div style='color: #ffcc00; margin-bottom: 10px; font-size: 13px;'>📈 <i>Romli lagi narik data dari Wall Street...</i></div>", unsafe_allow_html=True)
                hasil_bursa = cek_harga_kripto(pesan_terakhir["content"])
                pesan_groq.append({
                    "role": "system", 
                    "content": f"Berdasarkan data bursa resmi ini:\n{hasil_bursa}\n\nJawab pertanyaan user soal harga koin ini dengan gaya trader pro yang asik."
                })

                # --- JURUS SEKRETARIS (EMAIL) ---
            elif pilihan_alat == "📧 Kirim Email":
                st.markdown("<div style='color: #ffcc00; margin-bottom: 10px; font-size: 13px;'>📧 <i>Romli lagi nyiapin draf email...</i></div>", unsafe_allow_html=True)
                pesan_groq.append({
                "role": "system", 
                "content": "User ingin mengirim email. Buatlah draf pesannya. Di bagian BAWAH jawabanmu, WAJIB sertakan format:\n" + chr(96)*3 + "email\nTUJUAN: email@target.com\nSUBJEK: Judul Email\nPESAN: Isi pesan lengkap\n" + chr(96)*3
            })

            # --- KIRIM KE SERVER GROQ ---
            pesan_groq.insert(0, {"role": "system", "content": system_prompt})

            stream = client.chat.completions.create(
                model=model_aktif,
                messages=pesan_groq,
                stream=True
            )
            
            # Efek Ngetik Pelan-Pelan dengan Baju Romli
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_res += chunk.choices[0].delta.content
                    placeholder.markdown(f"<div class='romli-bubble'>{full_res}▌</div>", unsafe_allow_html=True)
            
            # ... (Kodingan efek ngetik Romli beres) ...
            placeholder.markdown(f"<div class='romli-bubble'>{full_res}</div>", unsafe_allow_html=True)
            
            # Simpan balasan ke memori
            st.session_state.messages.append({"role": "assistant", "content": full_res})

            # --- EKSEKUSI KODENYA JIKA MODE PYTHON AKTIF ---
            if pilihan_alat == "💻 Python":
                # Cari blok kode Python pakai Regex
                kodingan_ditemukan = re.findall(r'```python\n(.*?)\n```', full_res, re.DOTALL)
                
                if kodingan_ditemukan:
                    st.markdown("<div style='color: #ffcc00; margin-top: 10px; font-size: 13px;'>⚙️ <i>Romli sedang mengeksekusi kode di Pongo...</i></div>", unsafe_allow_html=True)
                    
                    for kode in kodingan_ditemukan:
                        hasil_terminal = jalankan_kode_python(kode)
                        
                        # Tampilkan hasil terminal ala kotak hitam hacker
                        st.code(hasil_terminal, language="text")
                        
                        # Simpan hasil terminal ini ke memori chat sebagai 'system'
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": f"**[Output Terminal Lokal]:**\n```text\n{hasil_terminal}\n```"
                        })

            elif pilihan_alat == "📧 Kirim Email":
                import re
                # Jaring Baja: Tangkep semua teks tanpa peduli format kotaknya
                # Jaring Titanium: Tangkep teks mau dia ngetik sebaris atau ke bawah
                # Jaring Sakti: Lebih toleran sama spasi, enter, atau teks tambahan
            email_match = re.search(r'TUJUAN:\s*([\w\.-]+@[\w\.-]+\.\w+).*?SUBJEK:\s*(.*?)\s*PESAN:\s*(.*)', full_res, re.DOTALL | re.IGNORECASE)

            if email_match:
            # --- GEMBOK LISENSI DIMULAI DARI SINI ---
            # Cek dulu, tier lu udah Plus/Pro/Multi belom?
               if st.session_state.tier_romli in ["Plus", "Pro", "Multi"]:
                
                # Kalau udah upgrade, baru jalanin emailnya
                tujuan = email_match.group(1).strip()
                subjek = email_match.group(2).strip()
                pesan = email_match.group(3).strip()
                
                hasil = kirim_email(tujuan, subjek, pesan)
                st.success(f"✅ {hasil}")
                
            else:
                # Kalau masih Basic, keluarin peringatan ini!
                st.error("🔒 Eits, tunggu dulu! Fitur Kirim Email cuma buat pengguna **Romli Plus** ke atas. Silakan Upgrade dulu di menu samping Ngab!")
            # --- GEMBOK LISENSI SELESAI ---
        except Exception as e:
            st.error(f"Saraf Mata Batin Putus: {e}")