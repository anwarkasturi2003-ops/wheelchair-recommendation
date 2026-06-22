import pandas as pd
import streamlit as st

st.set_page_config(page_title="Smart Wheelchair Recommendation System", page_icon="♿", layout="wide")

try:
    df = pd.read_csv("wheelchair_data.csv")
except Exception as e:
    st.error("❌ Ralat: Data csv gagal dimuatkan.")
    st.stop()

st.title("♿ Development of a Smart Wheelchair Recommendation System Based on Clinical Specification")
st.markdown("---")

col1, col2 = st.columns([1, 2])
with col1:
    st.header("📋 Borang Spesifikasi Klinikal")
    st.subheader("Data Pengguna / Pesakit")

    nama_pesakit = st.text_input("Nama Pesakit / ID:", value="Ahmad Bin Ali")
    berat_pesakit = st.number_input("Berat Badan Pesakit (kg):", min_value=10, max_value=250, value=65)

    st.markdown("**Ukuran Antropometri Klinikal (mm):**")
    lebar_pinggul = st.number_input("Lebar Pinggul Pesakit (Hip Width) (mm):", min_value=200, max_value=650, value=380)
    panjang_paha = st.number_input("Panjang Paha Pesakit (Thigh Length) (mm):", min_value=200, max_value=650, value=390)

    lebar_duduk_minimum = lebar_pinggul + 20
    kedalaman_duduk_minimum = panjang_paha + 20

    st.info(f"💡 **Keperluan Klinikal Minimum:**\n- Lebar Tempat Duduk $\\ge$ **{lebar_duduk_minimum} mm**\n- Kedalaman Tempat Duduk $\\ge$ **{kedalaman_duduk_minimum} mm**")
    butang_cari = st.button("🚀 Jana Rekomendasi Pintar", use_container_width=True)

with col2:
    st.header("🎯 Keputusan Padanan Model Kerusi Roda")
    hasil_tapis = df[(df['Max_User_Weight'] >= berat_pesakit) & (df['Nominal_Seat_Width'] >= lebar_duduk_minimum) & (df['Nominal_Seat_Depth'] >= kedalaman_duduk_minimum)]

    if butang_cari or not hasil_tapis.empty:
        st.success(f"Sistem menjumpai **{len(hasil_tapis)}** model kerusi roda dari pangkalan data yang 'tally' dengan keperluan klinikal pesakit.")

        paparan_df = hasil_tapis.rename(columns={
            "Series": "Siri", "Product_Name": "Nama Model / Siri",
            "Nominal_Seat_Width": "Lebar Tempat Duduk (mm)", "Nominal_Seat_Depth": "Kedalaman Tempat Duduk (mm)",
            "Front_Caster_Rear_Wheel": "Front caster / Rear wheel size (in)",
            "Backrest_Height": "Tinggi Penyandar (mm)", "Armrest_Seat_Dist": "Armrest to seat distance (mm)",
            "Footrest_Seat_Dist": "Footrest to seat distance (mm)", "Backrest_Angle": "Backrest angle (X°)",
            "Seat_Plane_Angle": "Seat plane angle (X°)", "Seat_Height_Front": "Seat surface height at front edge (mm)",
            "Leg_Seat_Angle": "Leg to seat angle (X°)", "Max_User_Weight": "Kapasiti Berat Maksimum (kg)",
            "Heaviest_Part_Mass": "Mass of the heaviest part (kg)", "Total_Mass": "Total mass (kg)",
            "Overall_Width": "Overall width (mm)", "Overall_Height": "Overall height (mm)",
            "Folded_Length": "Folded length (mm)", "Folded_Width": "Folded width (mm)",
            "Folded_Height": "Folded height (mm)", "Overall_Length": "Overall length with legrest (mm)"
        })
        st.dataframe(paparan_df, use_container_width=True)

        st.markdown("---")
        st.markdown("### 🏆 Cadangan Model Utama")
        model_terbaik = hasil_tapis.iloc[0] if not hasil_tapis.empty else df.iloc[0]
        st.subheader(f"🥇 {model_terbaik['Product_Name']}")
        st.markdown(f"Model ini disyorkan sebagai pilihan utama untuk pesakit **{nama_pesakit}** kerana saiznya yang ergonomik ({model_terbaik['Nominal_Seat_Width']}mm x {model_terbaik['Nominal_Seat_Depth']}mm) dan mampu menampung berat pesakit dengan selamat.")
    else:
        st.warning("⚠️ Tiada model padanan yang sesuai dengan kriteria yang dimasukkan.")
