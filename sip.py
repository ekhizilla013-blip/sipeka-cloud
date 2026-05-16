import streamlit as st
import pandas as pd
import os
import dropbox
from io import BytesIO

# --- KONFIGURASI UTAMA ---
st.set_page_config(page_title="SIPEKA CLOUD ULTIMATE", page_icon="☁️", layout="wide")

# 🔑 MASUKKAN TOKEN DROPBOX KAMU DI SINI:
DROPBOX_TOKEN = "sl.u.AGe5suTkhJtnR3ighqaRioChpqlcysLe1BEt9_35C4cFeV-5BtB12gAddpWU7J_arPLibtL-sgnEk_JgbFml3Wt9PQaRq___ZEZ8hzpVvgWrC1HAJAtKd39dYXQFs9mP9d0_s4Bxl66-GEEe1_ln3TNIiPqCVaBclwEcQ-zIpk_MYvyyOIgxShP1m7H8hlttskZhgB99Hh5SRhyzdkBal14K4uRkMtv1ErbmJXPjAJPMz6NTe1aB42qGOCKYqsk_a7CeJjJr69Gtv4Y7UbYSMg36745N4rTCpm5HY_sZq9Cre5mFnApbZd_eGNPdP_27ozg51Yn1yzegEP7qVUD_TZd0aKOR9pxxjOyEaCDbSMK-I9uMf4N-WQZ4Papf59ab9cnmBETp80iAmxIdGiNicogFlpKsYKVHB-H-KJNCfyUe2U2eFA-t_Cf3V4Xh750PVL0OZ8Z0lW3HivyjZl4BluJl4i67cUPTeKla-XYnTq78c5PMpQ18KO85pQL_EDfCjgHwL-AGQoJ-NayKA4vMeJpZukvPSXIIOhdE5jAnwXyMvNRF0io5bFPcvC-I0llzdiffuruvJY614Y5Uxq4hTIT3hzmK9DHf7fhPHjodNWwAy4gS-_CNkhoR_OTX_X800hupSHVGtPT62192Do0PH2WvWbnK-Q94D_Ky3d6VrHMXlN7lQjL_tqjuPHYBNPG2PZYtlpFGiQhqlv0hWjPFeYffSrP84mxCa9kf_biCTu5DXwgHyuMXfisyoSxhMBKv4bXFahB8Rv4y6jrMwpyY1qP002fQn6FK9gAHRnuW26nxgkTdRI8lKQr0j4TA0P2X5qUkQ61c3vDQwgPbv7GHkGhryHnm9TdNpsjsdVHG3j31Q9rWT47180hFUXnO6zfN3lyNWoXf5hxj9U2o14bNcysN55n7ocSAnX00elusVhXI-FZE6rwRenSyvc_mWOsu5F39GKP25yTQnwRjXGwuLra2x5tW50sae59bpTTX06AhkbqJAymA7qb8uD4TO8hUApA6aVNZ_vmRcbC4z0nbQ0efcRkSIuM_uFCMQVcYzg7zdFOFEnBiCKWD8O0_ItbOUXm_vrjzeE4oNilGElIjMbFleTNP1Dnn6WIANrxKnhWg04ChkrU7oLMkGl3agvGhuvdVD-tVYqvzg1yPqalELaNOGsGTNjxIOF8dEcL3YDHhr6f8IlJq9UewYQNJ2a_eZa3OHUoE1sIDwiH8IzFOxYIyaJ7yLiiAOxoTwJ8MyyElE7Qb-2D_9qjSmj6UzAoFTLud5Hn-1T3FWDYBbpvoqwNux3hlWkLVZTfZfBDiWoCsm1orrZHuFNRW5Rjrv32ctU2xOFJK1V3hA6SUOGVRXHY-xSdSsy1SmnqeJturefRzgXIQYMvpAKDWBPUuAO1En7CICSqdXiHdI5qfRuLxl-iH"

DB_FILE = "database_arsip.csv"
MEMO_FILE = "memo_internal.txt"

# Fungsi Hubungkan ke Dropbox
# Fungsi Hubungkan ke Dropbox (Versi Universal Sembuh Error)
def upload_ke_dropbox(file_data, file_name):
    try:
        dbx = dropbox.Dropbox(DROPBOX_TOKEN)
        path = f"/{file_name}"
        # 1. Upload file fisik ke folder Dropbox
        dbx.files_upload(file_data, path, mode=dropbox.files.WriteMode.overwrite)
        
        # 2. Taktik Cadangan bikin Link Publik langsung lewat fungsi basic
        link = dbx.sharing_create_shared_link_with_settings(path)
        
        # 3. Ubah biar langsung bisa di-preview di browser kedinasan
        return link.url.replace("?dl=0", "?raw=1")
    except Exception as e:
        st.error(f"Gagal Upload ke Dropbox: {e}")
        return "Gagal Upload"
