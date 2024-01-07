import pickle
import streamlit as st 
from streamlit_option_menu import option_menu
import pandas as pd 
import numpy as np

# Load Model
estimasi_model = pickle.load(open('lr-estimasi_harga_rumah_jaksel.sav', 'rb'))
hutang_model = pickle.load(open('dt-hutang-v1.sav', 'rb'))

#Navigasi Sidebar
with st.sidebar:
    #gambar = st.sidebar.image('icon\diabetes.png', width=100)
    selected = option_menu("Data Keuangan : ",
    ["Informasi","Estimasi Harga Rumah", "Prediksi Kredit"], icons=['microsoft-teams','house-add-fill', 'credit-card-2-back-fill'], menu_icon="file-bar-graph-fill", default_index=0)

if(selected=="Informasi"):
    # Judul
    st.title("Kelompok Data Mining")
    st.subheader("")
    st.subheader("Angota Kelompok:")
    st.subheader("")
    st.write("1. 21.240.0027 - Galih Dwi P.")
    st.write("2. 21.240.0025 - Nurul Murtadho")
    st.write("3. 21.240.0024 - Ade Rivaldy")
    st.write("4. 21.240.0014 - Muhammad Naufal P.")

if(selected=="Estimasi Harga Rumah"):
    # Judul
    st.title("Estimasi Harga Rumah Jakarta Selatan Menggunakan Regresi Linear")
    st.subheader("")

    # Membagi Kolom
    col1, col2 =st.columns(2)

    with col1:
        lt = st.number_input ("Jumlah Luas Tanah", format="%.0f", value=0.0, step=1.0)

    with col2:
        lb = st.number_input ("Jumlah Luas Bangunan", format="%.0f", value=0.0, step=1.0)

    with col1:
        jkt = st.number_input ("Jumlah Kamar Tidur", format="%.0f", value=0.0, step=1.0)

    with col2:
        jkm = st.number_input ("Jumlah Kamar Mandi", format="%.0f", value=0.0, step=1.0)

    pilihan = ['Ada', 'Tidak Ada']
    data_grs = st.selectbox('Opsi Garasi', pilihan, index=None, placeholder="...",)

    if data_grs == 'Ada':
        grs = 0
    else:
        grs = 1
    
    # Kode Prediksi

    estimasi_rumah = ''

    # Membuat Tombol
    if st.button('Cek Estimasi'):
        estimasi_prediksi = estimasi_model.predict([[lt, lb, jkt, jkm, grs]])
        st.write("Estimasi Harga Rumah Di Jakarta Selatan adalah Rp.", estimasi_prediksi) 
        
    # Data Input
    input = [lt, lb, jkt, jkm, grs, estimasi_rumah]

    # Output Dari Data Input
    st.write("")
    st.write("<p style='font-weight:bold'>Data Yang Baru Saja Anda Masukkan</p>", unsafe_allow_html=True)
    if input:
        columns = ['LT','LB','JKT','JKM','GRS','Estimasi Harga']
        df = pd.DataFrame([input], columns=columns)
        st.write(df)

    # DataFrame CSV
    st.write("")
    st.write("<p style='font-weight:bold'>DataFrame Untuk Kebutuhan Testing dan Training</p>", unsafe_allow_html=True)
    df = pd.read_csv("AnyConv.com__HARGA RUMAH JAKSEL.csv")
    st.write(df.head())

 # ------------------------------------------------------------------------------------------

if(selected=="Prediksi Kredit"):
    # Judul
    st.title("Prediksi Status Kredit Dengan Decision Tree")
    st.subheader("")

    no_of_dependents = st.slider ("Jumlah Tanggungan Pemohon", 0, 5)

    pilihan = ['Lulus', 'Tidak Lulus']
    data_edu = st.selectbox('Opsi Edukasi', pilihan, index=None, placeholder="...",)

    if data_edu == 'Lulus':
        edu = 0
    else:
        edu = 1

    pilihan = ['Ya', 'Tidak']
    data_se = st.selectbox('Opsi Wiraswasta:', pilihan, index=None, placeholder="...",)

    if data_se == 'Tidak':
        se = 0
    else:
        se = 1

    # Membagi Kolom
    col1, col2 =st.columns(2)
    
    with col1:
        income_annum = st.number_input ("Nilai Pendapatan Tahunan", format="%.0f", value=0.0, step=1.0, help="Contoh: 50")

    with col2:
        loan_amount = st.number_input ("Nilai Jumlah Pinjaman", format="%.0f", value=0.0, step=1.0)

    with col1:
        loan_term = st.number_input ("Jangka Waktu Pinjaman (Tahun)", format="%.0f", value=0.0, step=1.0)

    with col2:
        cibil_score = st.number_input ("Score Kredit", format="%.0f", value=0.0, step=1.0)

    with col1:
        residential_assets_value = st.number_input ("Nilai Aset Residensial", format="%.0f", value=0.0, step=1.0)

    with col2:
        commercial_assets_value = st.number_input ("Nilai Aset Komersial", format="%.0f", value=0.0, step=1.0)

    with col1:
        luxury_assets_value = st.number_input ("Nilai Aset Mewah", format="%.0f", value=0.0, step=1.0)

    with col2:
        bank_asset_value = st.number_input ("Nilai Aset Bank", format="%.0f", value=0.0, step=1.0)

    # Kode Prediksi

    pred_hutang = ''

    # Membuat Tombol
    if st.button('Test Prediksi'):
        hutang_prediksi = hutang_model.predict([[no_of_dependents, edu, se, income_annum,loan_amount,
                                                 loan_term,cibil_score, residential_assets_value,
                                                 commercial_assets_value, luxury_assets_value, 
                                                 bank_asset_value]])
        if hutang_prediksi[0] == 0:
                pred_hutang = "Status Penghutang Diterima Karena Data Sudah Mencukupi"
        else:
                pred_hutang = "Penghutang Ditolak Karena Data Belum Mencukupi Kebutuhan Yang Diminta"
        st.success(pred_hutang)  
        
    # Data Input
    input = [no_of_dependents, edu, se, income_annum,loan_amount,loan_term,cibil_score,
             residential_assets_value,commercial_assets_value,
             luxury_assets_value,bank_asset_value,pred_hutang]

    # Output Dari Data Input
    st.write("")
    st.write("<p style='font-weight:bold'>Data Yang Baru Saja Anda Masukkan</p>", unsafe_allow_html=True)
    if input:
        columns = ['no_of_dependents', 'education', 'self_employed','income_annum', 'loan_amount', 'loan_term', 'cibil_score',
                   'residential_assets_value', 'commercial_assets_value',
                   'luxury_assets_value', 'bank_asset_value','Status Hutang']
        df = pd.DataFrame([input], columns=columns)
        st.write(df)

    # Mengambil data dari file CSV
    st.write("")
    st.write("<p style='font-weight:bold'>DataFrame Untuk Kebutuhan Testing dan Training</p>", unsafe_allow_html=True)
    df = pd.read_csv("loan_approval_dataset.csv")
    st.write(df.head())
