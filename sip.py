import streamlit as st
import pandas as pd
import os
from PIL import Image
from io import BytesIO

# --- KONFIGURASI ---
st.set_page_config(page_title="SIPEKA CLOUD PRO", page_icon="☁️", layout="wide")

# Folder penyimpanan di Server Cloud (Internal Streamlit)
SAVE_FOLDER = "berkas_sipeka"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

DB_FILE = os.path.join(SAVE_FOLDER, "database_sipeka.csv")

def compress_image(uploaded_file):
    image = Image.open(uploaded_file)
    if image.mode in ("RGBA", "P"): image = image.convert("RGB")
    img_io = BytesIO()
    image.save(img_io, format="JPEG", quality=50, optimize=True)
    return img_io

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
    st.sidebar.success("✅ Cloud Storage Aktif")
    menu = st.sidebar.radio("NAVIGASI", ["📊 Statistik", "📤 Upload Berkas", "🔍 Database"])
    
    # Load Database
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
    else:
        df = pd.DataFrame(columns=["Tanggal", "Nama", "Kategori", "File"])

    if menu == "📊 Statistik":
        st.title("📊 Monitoring Digital")
        st.metric("Total Berkas Terarsip", len(df))
        if not df.empty:
            st.bar_chart(df['Kategori'].value_counts())

    elif menu == "📤 Upload Berkas":
        st.title("📤 Input Berkas Baru")
        with st.form("up"):
            nama = st.text_input("Judul/Nama Berkas")
            kat = st.selectbox("Kategori", ["Masuk", "Keluar", "SK", "Laporan"])
            f = st.file_uploader("Pilih Berkas (Gambar/PDF)")
            if st.form_submit_button("SIMPAN KE CLOUD"):
                if nama and f:
                    f_path = os.path.join(SAVE_FOLDER, f.name)
                    ext = os.path.splitext(f.name)[1].lower()
                    
                    # Kompres jika Gambar
                    if ext in ['.jpg', '.jpeg', '.png']:
                        proc = compress_image(f)
                        with open(f_path, "wb") as out: out.write(proc.getvalue())
                    else:
                        with open(f_path, "wb") as out: out.write(f.getbuffer())
                    
                    # Update Database
                    new_row = {"Tanggal": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"), "Nama": nama, "Kategori": kat, "File": f.name}
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    df.to_csv(DB_FILE, index=False)
                    st.success(f"✅ Berhasil! Berkas '{nama}' sudah aman di Cloud.")

    elif menu == "🔍 Database":
        st.title("🔍 Daftar Berkas Digital")
        if df.empty:
            st.info("Belum ada data.")
        else:
            st.dataframe(df, use_container_width=True)
            # Fitur Download Database
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Laporan CSV", data=csv, file_name="rekap_sipeka.csv", mime="text/csv")
