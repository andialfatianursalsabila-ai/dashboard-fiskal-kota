import streamlit as st
import pandas as pd

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Dashboard Data Fiskal Daerah Milik Alfatia",
    page_icon="💖",
    layout="wide"
)

# Custom Styling (CSS)
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
    }
    [data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: 700;
        color: #333333;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #2C3E50;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666666;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Load Data dari Github RAW
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Alam-A99/DATAAKSI/main/dataset_fiskal_97_hipoFull.csv"
    return pd.read_csv(url)

df = load_data()

# Sidebar - Filter Data
with st.sidebar:
    st.header("🔍 Filter Data")
    
    daftar_kota = df['Kota'].unique().tolist() if 'Kota' in df.columns else []
    kota_terpilih = st.multiselect(
        "Pilih Kota",
        options=daftar_kota,
        default=daftar_kota[:5] if daftar_kota else []
    )
    
    min_th = int(df['Tahun'].min()) if 'Tahun' in df.columns else 2014
    max_th = int(df['Tahun'].max()) if 'Tahun' in df.columns else 2024
    rentang_tahun = st.slider(
        "Rentang Tahun",
        min_value=min_th,
        max_value=max_th,
        value=(min_th, max_th)
    )
    
    st.divider()
    
    st.header("📊 Dashboard Fiskal")
    menu_terpilih = st.selectbox(
        "Pilih Menu",
        options=["Ringkasan", "Penerimaan Fiskal", "Belanja Pemerintah", "Indikator Sosial Ekonomi"]
    )

# Filter Dataframe
if 'Kota' in df.columns and 'Tahun' in df.columns:
    df_filtered = df[(df['Kota'].isin(kota_terpilih)) & (df['Tahun'].between(rentang_tahun[0], rentang_tahun[1]))]
else:
    df_filtered = df

# Header Utama
st.markdown('<h1 class="main-header">💖 Dashboard Data Fiskal Daerah Milik Alfatia</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Visualisasi data penerimaan fiskal, belanja pemerintah, dan indikator sosial ekonomi berdasarkan kota dan tahun.</p>', 
    unsafe_allow_html=True
)

st.divider()

# Ringkasan Metric (4 Kolom)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Jumlah Observasi", value=f"{len(df_filtered):,}")

with col2:
    n_kota = df_filtered['Kota'].nunique() if 'Kota' in df_filtered.columns else 0
    st.metric(label="Jumlah Kota", value=str(n_kota))

with col3:
    n_tahun = df_filtered['Tahun'].nunique() if 'Tahun' in df_filtered.columns else 0
    st.metric(label="Jumlah Tahun", value=str(n_tahun))

with col4:
    n_var = df_filtered.shape[1] if not df_filtered.empty else 0
    st.metric(label="Jumlah Variabel", value=str(n_var))

st.divider()

# Menampilkan Konten Berdasarkan Menu
if menu_terpilih == "Ringkasan":
    st.subheader("Ringkasan Data")
    st.dataframe(df_filtered, use_container_width=True)
elif menu_terpilih == "Penerimaan Fiskal":
    st.subheader("Visualisasi Penerimaan Fiskal")
    if 'PAD' in df_filtered.columns and 'Tahun' in df_filtered.columns:
        st.line_chart(df_filtered.groupby('Tahun')['PAD'].sum())
    else:
        st.dataframe(df_filtered, use_container_width=True)
elif menu_terpilih == "Belanja Pemerintah":
    st.subheader("Visualisasi Belanja Pemerintah")
    st.dataframe(df_filtered, use_container_width=True)
else:
    st.subheader("Indikator Sosial Ekonomi")
    st.dataframe(df_filtered, use_container_width=True)
