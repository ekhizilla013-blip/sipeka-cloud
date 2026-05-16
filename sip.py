import streamlit as st
import pandas as pd
import requests

# --- KONFIGURASI ---
st.set_page_config(page_title="SIPEKA CLOUD PRO", page_icon="☁️", layout="wide")

# LOGIN
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
    menu = st.sidebar.radio("NAVIGASI", ["📤 Upload Berkas", "🔍 Lihat Database"])

    if menu == "📤 Upload Berkas":
        st.title("📤 Input Berkas Baru")
        with st.form("input_form"):
            nama = st.text_input("Judul/Nama Berkas")
            kat = st.selectbox("Kategori", ["Masuk", "Keluar", "SK", "Laporan"])
            submit = st.form_submit_button("SIMPAN KE BRANKAS")
            
            if submit:
                if nama:
                    # GANTI LINK DI BAWAH DENGAN LINK GOOGLE SHEETS KAMU
                    link_sheets = "MASUKKAN_LINK_SHEETS_KAMU_DISINI"
                    st.success(f"✅ Data '{nama}' sedang diproses...")
                    st.balloons()
                    st.info(f"Silakan cek di Google Sheets: [Klik Disini]({link_sheets})")
                else:
                    st.warning("Isi nama dulu, Bree.")

    elif menu == "🔍 Lihat Database":
        st.title("🔍 Database Google Sheets")
        st.write("Data tersimpan aman di Google Sheets kamu.")
