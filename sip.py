import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- KONFIGURASI ---
st.set_page_config(page_title="SIPEKA CLOUD PRO", page_icon="☁️", layout="wide")

# GANTI INI DENGAN LINK GOOGLE SHEETS KAMU
URL_SHEET = "https://docs.google.com/spreadsheets/d/1nA5z4QXkMTRFuDGkhw7pjYtrAtz8K_rllRTj2nC86m8/edit?usp=sharing"

# Koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

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
    st.sidebar.success("✅ Terhubung ke Brankas Google")
    menu = st.sidebar.radio("NAVIGASI", ["📊 Statistik", "📤 Upload Berkas", "🔍 Database"])

    if menu == "📊 Statistik":
        st.title("📊 Monitoring Digital")
        data = conn.read(spreadsheet=URL_SHEET)
        st.metric("Total Berkas Terdaftar", len(data))
        if not data.empty:
            st.bar_chart(data['kategori'].value_counts())

    elif menu == "📤 Upload Berkas":
        st.title("📤 Input Berkas Baru")
        with st.form("input_form"):
            nama = st.text_input("Judul/Nama Berkas")
            kat = st.selectbox("Kategori", ["Masuk", "Keluar", "SK", "Laporan"])
            submit = st.form_submit_button("SIMPAN KE BRANKAS")
            
            if submit:
                if nama:
                    # Ambil data lama dari Sheets
                    existing_data = conn.read(spreadsheet=URL_SHEET)
                    # Tambah baris baru
                    new_row = pd.DataFrame([{
                        "tanggal": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
                        "nama": nama,
                        "kategori": kat,
                        "link file": "Tersimpan di sistem"
                    }])
                    updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                    # Kirim balik ke Google Sheets
                    conn.update(spreadsheet=URL_SHEET, data=updated_df)
                    st.success(f"✅ Mantap Bree! '{nama}' sudah masuk ke Google Sheets.")
                    st.balloons()
                else:
                    st.warning("Nama berkas jangan kosong ya.")

    elif menu == "🔍 Database":
        st.title("🔍 Database Google Sheets")
        data = conn.read(spreadsheet=URL_SHEET)
        st.dataframe(data, use_container_width=True)
        st.markdown(f"🔗 [Buka Google Sheets Langsung]({URL_SHEET})")
