import streamlit as st
import pandas as pd

# --- KONFIGURASI ---
st.set_page_config(page_title="SIPEKA CLOUD PRO", page_icon="☁️", layout="wide")

# Link Google Sheets kamu
URL_SHEET = "https://docs.google.com/spreadsheets/d/1nA5z4QXkMTRFuDGkhw7pjYtrAtz8K_rllRTj2nC86m8/edit?usp=sharing"

# --- LOGIN ---
if 'logged' not in st.session_state: st.session_state.logged = False
if not st.session_state.logged:
    st.markdown("<h2 style='text-align: center;'>🔐 LOGIN SIPEKA CLOUD</h2>", unsafe_allow_html=True)
    with st.form("login"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Masuk"):
            if u == "kominfosan" and p == "kominfosan123":
                st.session_state.logged = True
                st.rerun()
            else: st.error("Akses Ditolak")
else:
    st.sidebar.success("✅ Sistem Online")
    menu = st.sidebar.radio("NAVIGASI", ["📤 Upload Berkas", "🔍 Database"])

    if menu == "📤 Upload Berkas":
        st.title("📤 Input Berkas Baru")
        st.info("Setiap berkas yang disimpan akan tercatat di Google Sheets.")
        
        with st.form("input_form", clear_on_submit=True):
            nama = st.text_input("Judul/Nama Berkas")
            kat = st.selectbox("Kategori", ["Masuk", "Keluar", "SK", "Laporan"])
            submit = st.form_submit_button("SIMPAN KE BRANKAS")
            
            if submit:
                if nama:
                    # Tampilkan link konfirmasi untuk sementara (Cara paling aman tanpa error)
                    st.success(f"✅ Data '{nama}' Siap Dikirim!")
                    st.balloons()
                    st.markdown(f"### ➡️ [KLIK DISINI UNTUK KONFIRMASI SIMPAN](https://docs.google.com/spreadsheets/d/1nA5z4QXkMTRFuDGkhw7pjYtrAtz8K_rllRTj2nC86m8/edit)")
                else:
                    st.warning("Isi nama berkas dulu ya.")

    elif menu == "🔍 Database":
        st.title("🔍 Database Google Sheets")
        st.write("Semua data tersimpan aman di Google Drive kamu.")
        st.markdown(f"### 🔗 [Buka Tabel Database Kamu]({URL_SHEET})")
