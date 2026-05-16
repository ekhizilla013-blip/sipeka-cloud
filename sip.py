import streamlit as st
import pandas as pd
import os

# --- KONFIGURASI ---
st.set_page_config(page_title="SIPEKA CLOUD PRO", page_icon="☁️", layout="wide")

DB_FILE = "database_arsip.csv"

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
    st.sidebar.success("✅ Mode Cloud Aktif")
    menu = st.sidebar.radio("NAVIGASI", ["📤 Input Berkas", "🔍 Database & Laporan"])

    # Load Data
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
    else:
        df = pd.DataFrame(columns=["Tanggal", "Nama Berkas", "Kategori"])

    if menu == "📤 Input Berkas":
        st.title("📤 Input Berkas Baru")
        with st.form("input_manual", clear_on_submit=True):
            nama = st.text_input("Judul/Nama Berkas")
            kat = st.selectbox("Kategori", ["Masuk", "Keluar", "SK", "Laporan"])
            submit = st.form_submit_button("SIMPAN DATA")
            
            if submit:
                if nama:
                    new_row = pd.DataFrame([{"Tanggal": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"), "Nama Berkas": nama, "Kategori": kat}])
                    df = pd.concat([df, new_row], ignore_index=True)
                    df.to_csv(DB_FILE, index=False)
                    st.success(f"✅ Mantap Bree! '{nama}' sudah masuk database.")
                    st.balloons()
                else:
                    st.warning("Nama berkas kosong, Bree.")

    elif menu == "🔍 Database & Laporan":
        st.title("🔍 Monitoring Database")
        st.dataframe(df, use_container_width=True)
        
        st.divider()
        st.subheader("📥 Download Data untuk Laporan")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="DOWNLOAD EXCEL (CSV)",
            data=csv,
            file_name='rekap_sipeka_cloud.csv',
            mime='text/csv',
        )
        st.info("Klik tombol di atas untuk memindahkan data dari Cloud ke laptop kamu dalam bentuk Excel.")
