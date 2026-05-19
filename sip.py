import os
import sys
import subprocess

# --- AUTO INSTAL PUSTAKA ---
try:
    import gspread
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "gspread", "google-api-python-client"])
    import gspread

import streamlit as st
import pandas as pd
import time
from io import BytesIO
from google.oauth2.service_account import Credentials
import googleapiclient.discovery
import googleapiclient.http

# --- KONFIGURASI UTAMA ---
st.set_page_config(page_title="SIPEKA CLOUD ULTIMATE", page_icon="☁️", layout="wide")

GOOGLE_SHEET_NAME = "database sipeka master"
GOOGLE_DRIVE_FOLDER_ID = "1ggi3tUgFjefe3kzzbZFEy54b3OzUBtr6"

# 🔥 SISTEM BACA RAHASIA AMAN & BERSIH (FIXED PATH)
try:
    # Mengambil variabel langsung dari dalam grup [gcp_service_account]
    gcp_secrets = st.secrets["gcp_service_account"]
    
    credentials_dict = {
        "type": gcp_secrets["type"],
        "project_id": gcp_secrets["project_id"],
        "private_key_id": gcp_secrets["private_key_id"],
        "private_key": gcp_secrets["private_key"], 
        "client_email": gcp_secrets["client_email"],
        "client_id": gcp_secrets["client_id"],
        "auth_uri": gcp_secrets["auth_uri"],
        "token_uri": gcp_secrets["token_uri"],
        "auth_provider_x509_cert_url": gcp_secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": gcp_secrets["client_x509_cert_url"],
        "universe_domain": gcp_secrets["universe_domain"]
    }
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)
except Exception as e:
    st.error(f"Sistem gagal membaca konfigurasi rahasia: {e}")

def get_google_sheet():
    client = gspread.authorize(creds)
    return client.open(GOOGLE_SHEET_NAME).sheet1

def upload_ke_google_drive(file_bytes, file_name):
    try:
        service = googleapiclient.discovery.build('drive', 'v3', credentials=creds)
        file_metadata = {
            'name': file_name,
            'parents': [GOOGLE_DRIVE_FOLDER_ID]
        }
        media = googleapiclient.http.MediaIoBaseUpload(
            BytesIO(file_bytes), mimetype='application/octet-stream', resumable=True
        )
        file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        
        service.permissions().create(
            fileId=file.get('id'),
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()
        
        return file.get('webViewLink')
    except Exception as e:
        st.error(f"Gagal Simpan ke Google Drive: {e}")
        return "Gagal Upload"

def tampilkan_header():
    st.markdown("""
        <div style='text-align: center; padding-bottom: 20px;'>
            <h1 style='color: #a3e635; margin-bottom: 0;'>🏛️ SIPEKA CLOUD ULTIMATE</h1>
            <p style='color: #94a3b8; font-size: 16px; letter-spacing: 2px;'>KOMINFSAN DIGITAL ARCHIVE SYSTEM</p>
            <hr style='border-color: #1e293b;'>
        </div>
    """, unsafe_allow_html=True)

# --- LOGIN SYSTEM ---
if 'logged' not in st.session_state: st.session_state.logged = False

if not st.session_state.logged:
    tampilkan_header()
    st.markdown("<h3 style='text-align: center;'>🔐 KUNCI AKSES SISTEM</h3>", unsafe_allow_html=True)
    with st.form("login"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("MASUK KE CLOUD"):
            if u == "kominfosan" and p == "kominfosan123":
                st.session_state.logged = True
                st.rerun()
            else: st.error("Akses Ditolak! Periksa kembali Username & Password.")
else:
    st.sidebar.success("⚡ SIPEKA ONLINE (GOOGLE CLOUD MODE)")
    menu = st.sidebar.radio("NAVIGASI UTAMA", ["📤 Input Berkas Baru", "🔍 Database & Laporan"])
    
    if st.sidebar.button("🔒 LOGOUT / KELUAR SISTEM"):
        st.session_state.logged = False 
        st.rerun() 

    # --- AMBIL DATA DARI GOOGLE SHEET ---
    try:
        sheet = get_google_sheet()
        records = sheet.get_all_records()
        if records:
            df = pd.DataFrame(records)
        else:
            df = pd.DataFrame(columns=["Tanggal", "No Surat", "Perihal", "Kategori", "Link Berkas"])
    except Exception as e:
        st.error(f"Gagal terhubung ke Google Sheets: {e}")
        df = pd.DataFrame(columns=["Tanggal", "No Surat", "Perihal", "Kategori", "Link Berkas"])

    # --- MENU 1: INPUT BERKAS ---
    if menu == "📤 Input Berkas Baru":
        tampilkan_header()
        st.subheader("📤 Form Penginputan Berkas Resmi")
        
        with st.form("input_manual", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                no_surat = st.text_input("Nomor Surat", placeholder="Contoh: 005/123/KOMINFSAN/2026")
                kat = st.selectbox("Kategori Surat", ["Masuk", "Keluar", "SK", "Laporan", "Nota Dinas"])
            with col2:
                perihal = st.text_input("Perihal / Judul Berkas", placeholder="Contoh: Undangan Rapat Koordinasi")
            
            st.markdown("<br>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Pilih Berkas Lampiran (PDF, PNG, JPG)", type=["pdf", "png", "jpg", "jpeg"])
            submit = st.form_submit_button("🚀 SIMPAN PERMANEN KE GOOGLE CLOUD")
            
            if submit:
                if no_surat and perihal:
                    link_final = "Tidak Ada File"
                    if uploaded_file is not None:
                        with st.spinner(f"Mengunggah {uploaded_file.name} ke Google Drive..."):
                            link_final = upload_ke_google_drive(uploaded_file.read(), uploaded_file.name)
                    
                    waktu = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                    sheet.append_row([waktu, no_surat, perihal, kat, link_final])
                    
                    st.success(f"✅ Sukses Abadi! Data tersimpan di Google Cloud.")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("⚠️ Kolom 'Nomor Surat' dan 'Perihal' wajib diisi.")

    # --- MENU 2: DATABASE & LAPORAN ---
    elif menu == "🔍 Database & Laporan":
        tampilkan_header()
        st.subheader("🔍 Monitoring Kendali Arsip (Google Cloud Live Data)")
        
        search_query = st.text_input("🔍 Cari Surat Cepat...")
        df_display = df.copy()
        
        if search_query and not df_display.empty:
            df_display = df_display[df_display['No Surat'].astype(str).str.contains(search_query, case=False) | 
                                    df_display['Perihal'].astype(str).str.contains(search_query, case=False)]
        
        if not df_display.empty:
            st.data_editor(
                df_display,
                column_config={
                    "Link Berkas": st.column_config.LinkColumn("Link Berkas")
                },
                disabled=True,
                use_container_width=True
            )
        else:
            st.info("Database kosong atau belum ada data yang cocok."
