import streamlit as st
import json
import os

# Memuat data JSON
@st.cache_data
def load_data():
    with open("data_seni.json", "r", encoding="utf-8") as g:
        return json.load(g)

# Fungsi untuk menampilkan info lukisan dengan HTML + CSS
def tampil_lksn(l):
    col1, col2 = st.columns([1, 2])
    with col1:
        # Spacer HTML untuk menurunkan gambar secara presisi
        st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

        if "gambar" in l and os.path.exists(l["gambar"]):
            st.image(l["gambar"], width=200, caption=l["judul"])
        else:
            st.image("images/default.jpg", width=200, caption="(Gambar tidak tersedia)")

    with col2:
        st.markdown(f"""
        <div style="background-color:#0f0505; line-height: 1.0; padding:15px; border-radius:12px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
            <h4 style="color:#c71585;">🎨 {l['judul']}</h4>
            <p><strong>🧑‍🎨 Pelukis:</strong> {l['pelukis']}</p>
            <p><strong>📅 Tahun:</strong> {l['tahun']}</p>
            <p><strong>🎨 Gaya:</strong> {l['gaya']}</p>
            <p><strong>🖌️ Medium:</strong> {l['medium']}</p>
            <p><strong>📐 Ukuran:</strong> {l['ukuran']}</p>
            <p><strong>📍 Lokasi:</strong> {l['lokasi']}</p>
            <p><strong>📖 Deskripsi:</strong> {l['deskripsi']}</p>
        </div>
        """, unsafe_allow_html=True)

# Fungsi pencarian

def sequential_search_pelukis(data, keyword):
    hasil = []
    for zaman_idx, zaman in enumerate(data):
        for idx, lukisan in enumerate(zaman["lukisan"]):
            if keyword.lower() in lukisan["pelukis"].lower():
                hasil.append({
                    "zaman": zaman["zaman"],
                    "lukisan": lukisan,
                    "zaman_index": zaman_idx,
                    "lukisan_index": idx
                })
    return hasil

def sequential_search_judul(data, keyword):
    hasil = []
    for zaman_idx, zaman in enumerate(data):
        for idx, lukisan in enumerate(zaman["lukisan"]):
            if keyword.lower() in lukisan["judul"].lower():
                hasil.append({
                    "zaman": zaman["zaman"],
                    "lukisan": lukisan,
                    "zaman_index": zaman_idx,
                    "lukisan_index": idx
                })
    return hasil

# Konfigurasi Streamlit
st.set_page_config(page_title="Seni Lukis Berbagai Zaman", layout="wide")

st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        background-color: #0f0505;
        padding-top: 2rem;
    }
    h1, h2, h3, p {
        font-family: 'Segoe UI', sans-serif;
    }
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-thumb {
        background-color: #c71585;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='color:#c71585; font-size: 40px; font-weight: bold;'>
    Seni Lukis Berdasarkan Zaman
</h1> 
<p style='font-size:16px;'>Program ini menyajikan koleksi karya seni dari pelukis ternama mulai dari Neoklasik hingga era Modern.</p>
""", unsafe_allow_html=True)

data = load_data()
menu = st.sidebar.radio("Menu", ["Lihat berdasarkan zaman", "Cari Judul Lukisan", "Cari Nama Pelukis"])

# Menu 1 - Berdasarkan zaman
if menu == "Lihat berdasarkan zaman":
    zaman_list = [z["zaman"] for z in data]
    pilihan = st.selectbox("Pilih zaman seni:", zaman_list)

    for z in data:
        if z["zaman"] == pilihan:
            st.header(z["zaman"])
            st.markdown(f"**Deskripsi Zaman:** {z['deskripsi']}")
            st.subheader("Lukisan dari zaman ini:")
            for lukisan in z["lukisan"]:
                tampil_lksn(lukisan)

# Menu 2 - Cari Judul Lukisan
elif menu == "Cari Judul Lukisan":
    keyword = st.text_input("Masukkan judul lukisan")
    if keyword:
        hasil = sequential_search_judul(data, keyword)
        if hasil:
            st.success(f"Ditemukan {len(hasil)} lukisan dengan kata kunci: '{keyword}'")

            count_per_zaman = {}
            for item in hasil:
                count_per_zaman[item["zaman"]] = count_per_zaman.get(item["zaman"], 0) + 1

            for zaman, jumlah in count_per_zaman.items():
                st.markdown(f"**{zaman}**: {jumlah} lukisan")

            for item in hasil:
                tampil_lksn(item["lukisan"])
        else:
            st.error("Tidak ditemukan lukisan dengan judul tersebut.")

# Menu 3 - Cari Pelukis
elif menu == "Cari Nama Pelukis":
    keyword = st.text_input("Masukkan nama pelukis")
    if keyword:
        hasil = sequential_search_pelukis(data, keyword)
        if hasil:
            st.success(f"Ditemukan {len(hasil)} lukisan dari pelukis dengan nama: '{keyword}'")

            count_per_zaman = {}
            for item in hasil:
                count_per_zaman[item["zaman"]] = count_per_zaman.get(item["zaman"], 0) + 1

            for zaman, jumlah in count_per_zaman.items():
                st.markdown(f"**{zaman}**: {jumlah} lukisan")

            for item in hasil:
                tampil_lksn(item["lukisan"])
        else:
            st.error("Pelukis tidak ditemukan dalam daftar.")