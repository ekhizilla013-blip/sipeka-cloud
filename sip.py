import streamlit as st

# --- KONFIGURASI ---
st.set_page_config(page_title="SIPEKA CLOUD PRO", page_icon="☁️", layout="wide")

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
    st.sidebar.success("✅ Sistem Terintegrasi")
    menu = st.sidebar.radio("NAVIGASI", ["📤 Input Berkas", "🔍 Lihat Database"])

    if menu == "📤 Input Berkas":
        st.title("📤 Input Berkas Baru")
        st.write("Silakan isi formulir di bawah ini. Data akan langsung tersimpan di Google Sheets.")
        
        # GANTI LINK DI BAWAH INI DENGAN LINK 'KIRIM' GOOGLE FORM KAMU
        url_form = "MASUKKAN_LINK_GOOGLE_FORM_KAMU_DISINI"
        
        # Menampilkan Google Form di dalam Streamlit
        st.components.v1.iframe(url_form, height=800, scrolling=True)

    elif menu == "🔍 Lihat Database":
        st.title("🔍 Database Google Sheets")
        # GANTI LINK DI BAWAH INI DENGAN LINK GOOGLE SHEETS KAMU
        url_sheet = "https://docs.google.com/spreadsheets/d/1nA5z4QXkMTRFuDGkhw7pjYtrAtz8K_rllRTj2nC86m8/edit?usp=sharing"
        st.markdown(f"### 🔗 [KLIK DISINI UNTUK LIHAT DATA DI GOOGLE SHEETS]({url_sheet})")
        st.info("Gunakan link di atas untuk melihat rekapan data yang sudah masuk.")
