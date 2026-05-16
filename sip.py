import streamlit as st
import pandas as pd
import os
import dropbox
from io import BytesIO

# --- KONFIGURASI UTAMA ---
st.set_page_config(page_title="SIPEKA CLOUD ULTIMATE", page_icon="☁️", layout="wide")

# 🔑 MASUKKAN TOKEN DROPBOX KAMU DI SINI:
DROPBOX_TOKEN = "sl.u.AGeTW6W5FM4rtZ3rloKV4xZs3m4nQN4ZiT8nxEJiMZZpuXpYrwq2YRtxDXk19tNRZPpCP9JRk0OeCwrVweFzIhUHdVJkCAR-U7sEtkah5BcKB5EUO_kRRpzqehvQVli-ggQZ8a9q_w5iqnLhk9kxB2n4DgY6b5ijoS8sMGKlFZynT9EL2nVqygWF8rU8xyobMb_vuwAknhrDkkU3fIu76xxEqvKS6wLOR6jZAMHb8TwPLfU_WlV0piCUGdxg3RI9K1s9ruo2iFwftERX7_i4eQ9rYmPhdoH_O2qHk0IAzrBhzN-u4RF2SUAOHf6DRREHaVuZS0-w5ha_k6rP_MVZpgZQcK3ao_7SHRCCdC8RXHeVzUegmYkvG35mSmAk5Gmg8nGQQpHjxkeKh7JgDEFSvNjic5OSAgQI0of3_7URPcoEpYkKBR66_Vb_akjKC1NgGBBwcg3d6ALdXeYqGiPDeXN_Mek_zc4LPi661lLdZweqsAFuWU6DMnyowF6z2e3chqD2WiInVosmehhJbMVrr_zPfyXH0VCcV1rsPKPdIfGYOQfEn8k44aIbc5rKq0lbReNpUicQ5Us1glAqKv9ubBisys3ldY3g65HNiHZ0HHgQaKP5pw4zLdIGbu23dfhOvBEa48T0Izt7c0HZ1FxNCqNK68Zn7CkYvsE1AuYi8JeGVnUPntYycEYnOq4Lz9Q5jR3lwunvCCH2PAo9AK1auJaOPbriWzEYJLkbR9puYTz3zvK_Zuv2Sc0p3XdqY4YBrcWogcMGwk3QKc4UqJfY0Wi2wUvii0hm5aRzTbf1w8c30qtIl8oBovCBk6r_8wQ_ebJcnDTzTdZZTuJ9BHFFYo98eG0OxPVK8gX9VpJ5cewG1IDB8dLsmscijRcdm5xQue4st9pSmndvfdfDucPa2C3DjjQZRD8bUnSgv2ktMDV3GNqULef1WTPkoC6myRx0l8dGDRRSIiCNgsZrwv1EbNA1meehPv9Kl5mQRzhXRZz1aX_bUxquAdWldAmtJJ14e9gvvsmkyokW5ZjODtwMYrICzEMNk4TsdGEmNRf1v_JzIDjUs6AuvxBGL8w6UADN9IGOU9fFMIMbgJ3jViO7uxQiKkjDu5DscWh-W8VvlN5pyXW2jHtY9UjZFOqx9Nz1VJZsb5i4ngR-pNBj25Seiee0kMu0LSAcIxwPqhG2LR0NpdSvpAPoQ8ea6Khmg-MYUmDHWiRo0ABdsIYaGd0XxnLP-1EvDoGve819ru-0iBHmYrbkkrp3OmqFF2BxOjw2xrV8tKKcJeBquLAT-3IMLF1qaRpCrqIFtYxCDvToUJuZNBedejAd24a4iWkyB8emGs79eAavFcf2LYlek7wSX9ASkTFEKLGCmFqEcISEpm5FVGfKjnXyYzcY5dCKovI976xcqFeeNQrNmRulhk4Gzi9b"

DB_FILE = "database_arsip.csv"
MEMO_FILE = "memo_internal.txt"

# Fungsi Hubungkan ke Dropbox (Versi Fix Total)
def upload_ke_dropbox(file_data, file_name):
    try:
        dbx = dropbox.Dropbox(DROPBOX_TOKEN)
        path = f"/{file_name}"
        # 1. Upload file fisik ke folder Dropbox
        dbx.files_upload(file_data, path, mode=dropbox.files.WriteMode.overwrite)
        # 2. Bikin Link Publik
        link = dbx.sharing_create_shared_link_with_settings(path)
        # 3. Ubah biar langsung bisa di-preview di browser kedinasan
        return link.url.replace("?dl=0", "?raw=1")
    except Exception as e:
        st.error(f"Gagal Upload ke Dropbox: {e}")
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
        df = pd.DataFrame(columns=["Tanggal", "No Surat", "Perihal", "Kategori", "Link Berkas"])

    if "Link Berkas" not in df.columns:
        df["Link Berkas"] = "Tidak Ada File"

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
            st.markdown("<h5 style='color: #22d3ee;'>⚙️ REAL CLOUD STORAGE INTEGRATION</h5>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Pilih Berkas Lampiran (PDF, PNG, JPG, PPTX)", type=["pdf", "png", "jpg", "jpeg", "pptx", "docx"])
            
            submit = st.form_submit_button("🚀 SIMPAN & UNGGAH BERKAS KE CLOUD")
            
            if submit:
                if no_surat and perihal:
                    link_final = "Tidak Ada File"
                    
                    if uploaded_file is not None:
                        with st.spinner(f"Sedang mengirim {uploaded_file.name} ke Cloud Storage..."):
                            file_bytes = uploaded_file.read()
                            link_final = upload_ke_dropbox(file_bytes, uploaded_file.name)
                    
                    new_row = pd.DataFrame([{
                        "Tanggal": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"), 
                        "No Surat": no_surat, 
                        "Perihal": perihal, 
                        "Kategori": kat,
                        "Link Berkas": link_final
                    }])
                    df = pd.concat([df, new_row], ignore_index=True)
                    df.to_csv(DB_FILE, index=False)
                    st.success(f"✅ Sukses Total! Data & Berkas Fisik Berhasil Dikunci di Cloud.")
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
        search_query = st.text_input("🔍 Cari Surat Cepat...")
        
        df_display = df.copy()
        
        if search_query:
            df_display = df_display[df_display['No Surat'].astype(str).str.contains(search_query, case=False) | 
                                    df_display['Perihal'].astype(str).str.contains(search_query, case=False)]
        
        # Menampilkan tabel dengan link aktif
        st.data_editor(
            df_display,
            column_config={
                "Link Berkas": st.column_config.LinkColumn(
                    "Link Berkas",
                    help="Klik link untuk membuka atau download dokumen fisik",
                    max_chars=1000,
                )
            },
            disabled=True,
            use_container_width=True
        )
        
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
                    st.error(f"🗑️ Sukses! Surat No '{pilihan_hapus}' telah dihapus.")
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

    # --- MENU 3: RUANG CATATAN / MEMO INTERNAL ---
    elif menu == "📝 Ruang Catatan/Memo":
        tampilkan_header()
        st.subheader("📝 Memo & Catatan Internal Staf")
        
        if os.path.exists(MEMO_FILE):
            with open(MEMO_FILE, "r") as f:
                memo_lama = f.read()
        else:
            memo_lama = "Belum ada catatan malam ini."
            
        st.text_area("🗒️ Catatan Saat Ini:", value=memo_lama, height=200, disabled=True)
        
        with st.form("form_memo", clear_on_submit=True):
            isi_memo = st.text_input("Ketik catatan baru di sini...")
            simpan_memo = st.form_submit_button("✍️ Tambahkan ke Catatan")
            
            if simpan_memo and isi_memo:
                waktu = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                format_baru = f"[{waktu}] Staf: {isi_memo}\n"
                with open(MEMO_FILE, "a") as f:
                    f.write(format_baru)
                st.success("📝 Catatan berhasil ditambahkan!")
                st.rerun()
