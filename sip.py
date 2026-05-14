import streamlit as st
import pandas as pd
import os
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="SIPEKA CLOUD PRO", page_icon="☁️", layout="wide")
SAVE_FOLDER = "/Users/ekhi/Library/CloudStorage/GoogleDrive-ekhi.zilla013@gmail.com/Drive Saya/SIPEKA_DRIVE"
DB_FILE = os.path.join(SAVE_FOLDER, "database_sipeka.csv")

def compress_image(uploaded_file):
    image = Image.open(uploaded_file)
    if image.mode in ("RGBA", "P"): image = image.convert("RGB")
    img_io = BytesIO()
    image.save(img_io, format="JPEG", quality=50, optimize=True)
    return img_io

if 'logged' not in st.session_state: st.session_state.logged = False
if not st.session_state.logged:
    st.markdown("<h2 style='text-align: center;'>🔐 LOGIN SIPEKA</h2>", unsafe_allow_html=True)
    with st.form("login"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Masuk"):
            if u == "kominfosan" and p == "kominfosan123":
                st.session_state.logged = True
                st.rerun()
            else: st.error("Akses Ditolak!")
else:
    st.sidebar.success("✅ Terhubung ke Google Drive")
    st.sidebar.info("🚀 Mode Hemat Cloud Aktif")
    menu = st.sidebar.radio("MENU", ["📊 Statistik", "📤 Upload Berkas", "🔍 Database"])
    
    if not os.path.exists(SAVE_FOLDER):
        st.error("❌ Folder tidak ditemukan! Pastikan Google Drive aktif.")
    else:
        df = pd.read_csv(DB_FILE) if os.path.exists(DB_FILE) else pd.DataFrame(columns=["Tanggal", "Nama", "Kategori", "File"])
        if menu == "📊 Statistik":
            st.title("📊 Monitoring Digital")
            st.metric("Total Berkas", len(df))
            if not df.empty: st.bar_chart(df['Kategori'].value_counts())
        elif menu == "📤 Upload Berkas":
            st.title("📤 Simpan ke Cloud (Auto-Compress)")
            with st.form("up"):
                nama = st.text_input("Judul Berkas")
                kat = st.selectbox("Kategori", ["Masuk", "Keluar", "SK", "Laporan"])
                f = st.file_uploader("Pilih Berkas")
                if st.form_submit_button("SINKRON"):
                    if nama and f:
                        f_path = os.path.join(SAVE_FOLDER, f.name)
                        ext = os.path.splitext(f.name)[1].lower()
                        if ext in ['.jpg', '.jpeg', '.png']:
                            proc = compress_image(f)
                            with open(f_path, "wb") as out: out.write(proc.getvalue())
                        else:
                            with open(f_path, "wb") as out: out.write(f.getbuffer())
                        new_row = {"Tanggal": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"), "Nama": nama, "Kategori": kat, "File": f.name}
                        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                        df.to_csv(DB_FILE, index=False)
                        st.success("✅ Berhasil disimpan!")
        elif menu == "🔍 Database":
            st.title("🔍 Database Digital")
            st.table(df)
