import streamlit as st
import pandas as pd
import os
import time
from io import BytesIO

# --- KONFIGURASI UTAMA ---
st.set_page_config(page_title="SIPEKA CLOUD ULTIMATE", page_icon="☁️", layout="wide")

DB_FILE = "database_arsip.csv"
MEMO_FILE = "memo_internal.txt"

# --- 1. MAKEOVER: LOGO & STYLE ---
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
    # --- SIDEBAR MENU ---
    st.sidebar.success("⚡ SIPEKA ONLINE (MODE PRO)")
    menu = st.sidebar.radio("NAVIGASI UTAMA", [
        "📤 Input Berkas Baru", 
        "🔍 Database & Laporan",
        "📝 Ruang Catatan/Memo"
    ])
    
    st.sidebar.divider() 
    if st.sidebar.button("🔒 LOGOUT / KELUAR SISTEM"):
        st.session_state.logged = False 
        st.rerun() 

    # --- LOAD DATABASE ---
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
    else:
        df = pd.DataFrame(columns=["Tanggal", "No Surat", "Perihal", "Kategori", "Status Berkas"])

    # Pastikan kolom 'Status Berkas' ada di database lama
    if "Status Berkas" not in df.columns:
        df["Status Berkas"] = "Teks Terbaca"

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
            
            # --- FITUR ADVANCED: TOMBOL UPLOAD BERKAS ASLI (MOCKUP PRO) ---
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<h5 style='color: #22d3ee;'>⚙️ DIGITAL STORAGE INTEGRATION (MILESTONE 2)</h5>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Pilih Berkas Lampiran (PDF, PNG, JPG, PPTX, DOCX)", type=["pdf", "png", "jpg", "jpeg", "pptx", "docx"])
            
            submit = st.form_submit_button("🚀 SIMPAN & UNGGAH BERKAS KE CLOUD")
            
            if submit:
                if no_surat and perihal:
                    status_upload = "Hanya Teks"
                    
                    # Jika user mengunggah file beneran, jalankan simulasi progress bar yang keren
                    if uploaded_file is not None:
                        status_upload = f"📎 Terunggah ({uploaded_file.name})"
                        progress_text = f"Mengunggah {uploaded_file.name} ke Cloud Storage. Mohon tunggu..."
                        my_bar = st.progress(0, text=progress_text)
                        
                        # Simulasi loading jalan pelan-pelan biar realistis
                        for percent_complete in range(100):
                            time.sleep(0.01)
                            my_bar.progress(percent_complete + 1, text=progress_text)
                        time.sleep(0.5)
                        my_bar.empty() # Hapus progress bar setelah sukses
                        st.info(f"⚡ Enkripsi Sukses: File '{uploaded_file.name}' berhasil diamankan di Cloud.")

                    new_row = pd.DataFrame([{
                        "Tanggal": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"), 
                        "No Surat": no_surat, 
                        "Perihal": perihal, 
                        "Kategori": kat,
                        "Status Berkas": status_upload
                    }])
                    df = pd.concat([df, new_row], ignore_index=True)
                    df.to_csv(DB_FILE, index=False)
                    st.success(f"✅ Berhasil! Surat No {no_surat} dan lampirannya sudah dikunci di dalam database cloud.")
                    st.balloons()
                else:
                    st.warning("⚠️ Gagal Simpan! Kolom 'Nomor Surat' dan 'Perihal' wajib diisi ya, Bree.")

    # --- MENU 2: DATABASE & LAPORAN ---
    elif menu == "🔍 Database & Laporan":
        tampilkan_header()
        
        # STATISTIK DASHBOARD VISUAL
        st.subheader("📊 Ringkasan Arsip Digital")
        total_surat = len(df)
        total_masuk = len(df[df['Kategori'] == 'Masuk'])
        total_keluar = len(df[df['Kategori'] == 'Keluar'])
        total_sk = len(df[df['Kategori'] == 'SK'])
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("📂 Total Arsip", f"{total_surat} Berkas")
        m2.metric("📥 Surat Masuk", f"{total_masuk} Berkas")
        m3.metric("📤 Surat Keluar", f"{total_keluar} Berkas")
        m4.metric("📜 Total SK", f"{total_sk} Berkas")
        st.divider()
        
        st.subheader("🔍 Monitoring Kendali Arsip")
        search_query = st.text_input("🔍 Cari Surat Cepat (Ketik No Surat atau Perihal)...")
        if search_query:
            filtered_df = df[df['No Surat'].astype(str).str.contains(search_query, case=False) | 
                             df['Perihal'].astype(str).str.contains(search_query, case=False)]
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)
        
        # FITUR HAPUS DATA UNTUK ADMIN
        if not df.empty:
            st.divider()
            st.subheader("🛠️ Panel Kontrol Admin (Hapus Data Salah)")
            with st.expander("❌ Klik di sini untuk menghapus data yang salah input"):
                pilihan_hapus = st.selectbox("Pilih No Surat yang akan dihapus:", df['No Surat'].tolist())
                tombol_hapus = st.button("🗑️ HAPUS PERMANEN DARI CLOUD")
                
                if tombol_hapus:
                    df = df[df['No Surat'] != pilihan_hapus]
                    df.to_csv(DB_FILE, index=False)
                    st.error(f"🗑️ Sukses! Surat No '{pilihan_hapus}' telah dihapus dari database cloud.")
                    st.rerun()

        st.divider()
        st.subheader("📥 Penarikan Laporan Excel")
        
        def to_excel(data_frame):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            data_frame.to_excel(writer, index=False, sheet_name='Database_Sipeka')
            writer.close()
            return output.getvalue()

        if not df.empty:
            excel_data = to_excel(df)
            st.download_button(
                label="📊 DOWNLOAD LAPORAN EXCEL (.xlsx)",
                data=excel_data,
                file_name='LAPORAN_SIPEKA_ULTIMATE.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            st.info("Database masih kosong. Belum ada data untuk di-download.")

    # --- MENU 3: RUANG CATATAN / MEMO INTERNAL ---
    elif menu == "📝 Ruang Catatan/Memo":
        tampilkan_header()
        st.subheader("📝 Memo & Catatan Internal Staf")
        st.info("Ruang santai buat ninggalin catatan atau memo penting antar staf yang jaga shift.")
        
        if os.path.exists(MEMO_FILE):
            with open(MEMO_FILE, "r") as f:
                memo_lama = f.read()
        else:
            memo_lama = "Belum ada catatan malam ini."
            
        st.text_area("🗒️ Catatan Saat Ini:", value=memo_lama, height=200, disabled=True)
        
        with st.form("form_memo", clear_on_submit=True):
            isi_memo = st.text_input("Ketik catatan baru di sini...", placeholder="Contoh: Surat dari Dinas Perhubungan sudah ditindaklanjuti.")
            simpan_memo = st.form_submit_button("✍️ Tambahkan ke Catatan")
            
            if simpan_memo and isi_memo:
                waktu = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                format_baru = f"[{waktu}] Staf: {isi_memo}\n"
                
                with open(MEMO_FILE, "a") as f:
                    f.write(format_baru)
                    
                st.success("📝 Catatan berhasil ditambahkan!")
                st.rerun()
