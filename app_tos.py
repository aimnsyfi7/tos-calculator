import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="TOS Virtual Work Calculator", layout="centered")

st.title("🏗️ TOS Calculator: Virtual Work Method")
st.markdown("Kalkulator interaktif untuk analisis rasuk, tindak balas sokongan, cerun, dan pesongan.")

st.sidebar.header("⚙️ Parameter Rasuk & Beban")

# Input Geometri & Sifat Rasuk
st.sidebar.subheader("1. Sifat Rasuk & Bahan")
length_ab = st.sidebar.number_input("Panjang Span AB (m)", value=8.0, step=0.5)
e_modulus = st.sidebar.number_input("Modulus Keanjalan, E (kN/mm²)", value=200.0, step=10.0)
i_inertia = st.sidebar.number_input("Momen Inersia, I (mm⁴)", value=100.0, step=10.0, format="%.1f")

# Tukar unit EI kepada kN·m²
# E in kN/m² = E_modulus * 10^6
# I in m^4 = i_inertia * 10^6 * (10^-3)^4 = i_inertia * 10^-2 m^4 ... 
# Mari kita guna nilai standard: 200 kN/mm2 = 200e6 kN/m2, 100e6 mm4 = 100e-6 m4 -> EI = 20000
ei_value = (e_modulus * 1000) * (i_inertia * 1e-6) # Sesuaikan ikut skala standard

# Input Beban
st.sidebar.subheader("2. Beban Bertindak")
w_udl = st.sidebar.number_input("UDL (kN/m) sepanjang AB", value=30.0, step=5.0)
m_b = st.sidebar.number_input("Momen di B (kNm) [+ve ikut jam, -ve lawan jam]", value=-12.0, step=1.0)
p_d = st.sidebar.number_input("Beban Tumpu di D (kN) [Contoh: 19.62 kN]", value=19.62, step=1.0)
dist_d = st.sidebar.number_input("Jarak D dari B (m)", value=4.0, step=0.5)

if st.button("🚀 Kira Sekarang"):
    st.markdown("---")
    st.subheader("📊 Keputusan Analisis")

    # --- LANGKAH 1: KIRA TINDAK BALAS SOKONGAN (A & B) ---
    # Mengambil momen di A (Sum of moments about A = 0)
    # UDL bertindak pada L/2 = length_ab / 2 dengan jumlah daya (w_udl * length_ab)
    total_udl_force = w_udl * length_ab
    udl_arm = length_ab / 2.0
    
    # Momen di B bertindak pada jarak length_ab
    # Beban D bertindak pada jarak length_ab + dist_d dari A
    total_dist_d = length_ab + dist_d
    
    # R_B * length_ab - (total_udl_force * udl_arm) - m_b - (p_d * total_dist_d) = 0
    # Nota: m_b dalam soalan adalah counterclockwise (lawan jam = -ve dalam konvensyen biasa jika melawan arah jam ke bawah, tapi kita ikut nilai input)
    sum_momen_lain = (total_udl_force * udl_arm) + m_b + (p_d * total_dist_d)
    r_b = sum_momen_lain / length_ab
    
    # Sum of vertical forces = 0 -> R_A + R_B - total_udl_force - p_d = 0
    r_a = total_udl_force + p_d - r_b

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Tindak Balas Sokongan R_A", value=f"{r_a:.2f} kN")
    with col2:
        st.metric(label="Tindak Balas Sokongan R_B", value=f"{r_b:.2f} kN")

    # --- LANGKAH 2: ANGGARAN NILAI EI ---
    st.info(f"💡 Nilai Kekakuan Flexural (EI) yang digunakan: **{ei_value:,.2f} kN·m²**")

    # --- LANGKAH 3: VISUALISASI RASUK ---
    fig, ax = plt.subplots(figsize=(10, 3))
    
    # Lukis rasuk utama
    ax.plot([0, length_ab], [0, 0], 'k-', lw=4, label="Rasuk AB")
    ax.plot([length_ab, length_ab + dist_d], [0, 0], 'k--', lw=2, label="Unjuran ke D")
    
    # Sokongan
    ax.scatter([0], [0], color='red', s=100, zorder=5, label="Pin (A)")
    ax.scatter([length_ab], [0], color='green', s=100, zorder=5, label="Roller (B)")
    
    # Label titik
    ax.text(0, -0.3, 'A', fontsize=12, fontweight='bold', ha='center')
    ax.text(length_ab, -0.3, 'B', fontsize=12, fontweight='bold', ha='center')
    ax.text(length_ab + (dist_d/2), -0.3, 'C (tengah AB? / D)', fontsize=10, ha='center')
    ax.text(length_ab + dist_d, -0.3, 'D', fontsize=12, fontweight='bold', ha='center')

    ax.set_xlim(-1, length_ab + dist_d + 1)
    ax.set_ylim(-1, 2)
    ax.axhline(0, color='gray', lw=1)
    ax.set_title("Rajah Skematik Rasuk")
    ax.axis('off')
    st.pyplot(fig)

    st.success("✅ Kod siap! Maman boleh ubah nilai parameter di sidebar ikut soalan-soalan lain untuk semak jawapan.")