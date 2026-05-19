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
import base64
import json
from io import BytesIO
from google.oauth2.service_account import Credentials
import googleapiclient.discovery
import googleapiclient.http

# --- KONFIGURASI UTAMA ---
st.set_page_config(page_title="SIPEKA CLOUD ULTIMATE", page_icon="☁️", layout="wide")

GOOGLE_SHEET_NAME = "database sipeka master"
GOOGLE_DRIVE_FOLDER_ID = "1ggi3tUgFjefe3kzzbZFEy54b3OzUBtr6"

# 🔑 KUNCI JALUR BASE64 (ANTI ACAL-ACAK FORMAT)
ENCODED_KEY = "eyJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsICJwcm9qZWN0X2lkIjogImZyZXNoLXNlbnNvci00OTY3MDUtZDkiLCAicHJpdmF0ZV9rZXlfaWQiOiAiNmU1MWEzYjE5YzFlOWViODgwNDAzN2E5MGQwMzVhM2YxMzEyODc3NCIsICJwcml2YXRlX2tleSI6ICItLS0tLUJFR0lOIFBSSVZBVEUgS0VZLS0tLS1cbk1JSUV2d0lCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQktsd2dnU2xBZ0VBQW9JQkFRRGpERWI1TUI2T1dyRXdcbjJJYVJWallHODNPZzlFbVk1TklDRkxqR2RVeHpEdUFHNzBNeDlWQ3lWKzBreTZpcHRLVXlOQzM4TjFCZmd1TkJcbisstructuralY3pVZEN6Q3VXS2VtWHVFSlFLbE1xTXk4WW1SbzJsaWtKejRD crappyRzMxbTFabmJlQWpXQXArWUwxb1BceEVpUUtNY013N3lva0c5Z2RiOHVPVDE1ZFlIdmpPVmQvWTZvQUV3WU90eG1wNEtIME5vSlZwWmVzM3FzSVRjTlxub1NWalRmbURpaFN1ajcyNjJQTS9yaExTK2FnZTd1S2dhNHoxNDJ2bHFwbDY1QjcyWFh6YmJhbXVMNm80OG9LY1xudlhHMmpDQT crappyVVWlxenlhZ2x4djcrK0lxMlBGS3AyZGRIeWoySnNmUGsxSzd6dXBHOFg2bEM3VlZJakVBRVYzZlx1UlIvUFNkRkhBZ01CQUFFQ2dnRUFPNVo0S0NEd1pka0RpQlVVTnc4SCtpeGpwVi9WWHVNeTU4SzRwWUdaN0R5XG5VQzdoVmtDa3JaWVBmZjhseFFXbFFIYTVyRW9Ia2dCVHltMjI1TWNFejFtTUlGSW1jRTZRVG9KSkZWK1BqTGdqXG5VaVB2VnIzdWw0cGYvTUdYUG9ZekZYSzhNc2ZBVDd4dlFqd3VKUHAwWmZCSjNZRzZGNjlTY0UwcXFPTWVsbXA5XG4xR2hyajhUc3ZzRFozV1ZkZzhjaGlLeENtcldHQnp6eitGTWxEOXFRemQ5QURoMHomL3VJQTZBSHFCV1V0NjZcbkNTSEN5cWZ5L3h4WVkyNmZUbjJVbUh4aTFoUllHZ0lLTDBaNmEvcGZHUlpnNW4vY3pvRnpBNEtMbWhzSzh6cHJcbnU0NjJnT0pORDVzYzBOWXRuYjNQMmU4WTdEMS9mZWJwMnNYQW5QZWM0UUtCZ1FENGpZVzZ2Z0Y2anhYN2xmaVxucVZPU0dMeE1sSnE3VFN4Y3ZoTDdyaUVWQ3hMMDFGaXJBMnVCV0RmNzZKT1JDWS9OK2pVczRkeXQwTnkwek5WalxudllkZDF1MDV2QzRDVndYK0JJcDY2S2wwcWhhTGpuZkJ0MG93VDVyVytaZW90RStOemVrdHlYcVhjWnowTEU0XG5LYmF5aFdQT1hCQkZ6N0hiWTZpK1lmSGpad0tCZ1FEcG5hYm9laDlXUTlCeTBsanlHOVhvQVNXM3hleXc0ZnlnXG5LTnh4M1ZnbUpWa25ydVZIYWlqbWtwU2RqVnhqcUp4dFl6eEZiMFFBaHdkRllXclNROEhlM1FZb0pYUnlxMjNcbmJBTFVTSUpzbE5jUzlkaXFvRncvSDZaYW8zSk5Ba3RBdjdMWmkyeWZCTUhLRDV6bEFDY2M2R21qVklidmVMTUhcbjZwOXhHZURYSVFLQmdRQ3FYTGhFRFZVUDRpbXVGQUxUcmxRT0JxZnczQlJ6U2kybE4zVnlKbEo2d0ZVeVFYQXBcbmNVY01veVp2ZEQrUEVXNGJ3Y2JsZTZhSzBpZzlwYmNELzhRVUNsWVhvWFh6bmpqNUxZelBxNmhVdlI2QTRzVzNcdmZTdGJlUzlTQmlYRm0rbVpWTFJreDZML3JzRzJZZURuYnhDdGZzN1BmNVNZNk5XRlB1Rk5zMjFZNHdLQmdRQ1Rcbldjcm9uL1haMitYQ05objJzaFhGUWN2L1QrZU1YTXlRVzVWR2Y5dlVYUHhwYWdjVWhoYlBPTEViaUljcHRlQS8rXG45Z29TR0tycFNOdGdnSzJSTGdCR2FiNzh0WFFvM3pzLzMvRWM0U3JadnpxenU3bmZURXRDUzA1ViswRWVyN2kwXG4rdk9jQURNZlRNbkpYdlZPL2ZueXcwT3RqMmVWWnNoTWF1L3JUdTRmNFFLQmdRQ3ZTR0dGUjlMbDJzQWduQklXXG54djE4d2orOGQxUFdXbk1EZXBFTlZhQTFpMWhpZGtaQlBNVGdPU0UrQVdqS2RKZzMxdDQvR3N6RGhGdlA0MEF2XG5DbHBaOEdkL21QejJtVXJlZWNONjYzUklWTVJna0VvVG9RRXVzdm96cTZsU3ltNmZIQTdoM0Y3SklMYXRXVStcbndzbzc2WFBtZFhkMWJacmJ5K0Rnd0ZSbCtBPT1cbi0tLS0tRU5EIFBSSVZBVEUgS0VaLS0tLS1cbiIsICJjbGllbnRfZW1haWwiOiAia3VyaXItc2lwZWthQGZyZXNoLXNlbnNvci00OTY3MDUtZDkuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCAiY2xpZW50X2lkIjogIjExMDU5NDkzODA1NTcxNDc3NzQ2MCIsICJhdXRoX3VyaSI6ICJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20vby9vYXV0aDIvYXV0aCIsICJ0b2tlbl91cmkiOiAiaHR0cHM6Ly9vYXV0aDIuZ29vZ2xlYXBpcy5jb20vdG9rZW4iLCAiYXV0aF9wcm92aWRlcl94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL29hdXRoMi92MS9jZXJ0cyIsICJjbGllbnRfeDUwOV9jZXJ0X3VybCI6ICJodHRwczovL3d3dy5nb29nbGVhcGlzLmNvbS9vYXV0aDIvdjEvY2VydHMvY3VyaXItc2lwZWthJTQ0ZnJlc2gtc2Vuc29yLTQ5NjcwNS1kOS5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsICJ1bml2ZXJzZV9kb21haW4iOiAiZ29vZ2xlYXBpcy5jb20ifQ=="

try:
    # Decode Base64 balik ke teks JSON murni aslinya
    decoded_bytes = base64.b64decode(ENCODED_KEY)
    credentials_dict = json.loads(decoded_bytes.decode('utf-8'))
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)
except Exception as e:
    st.error(f"Sistem gagal membaca dekripsi rahasia: {e}")

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
            st.info("Database kosong atau belum ada data yang cocok.")
