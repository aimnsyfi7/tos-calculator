import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="TOS Dynamic Ultimate Calculator", layout="wide")

st.title("🏗️ TOS Dynamic Structural Calculator & Formula Sheet")
st.markdown("Kalkulator Analisis Struktur (TOS) dengan tetapan titik beban dinamik dan komponen sudut (angle).")

tab1, tab2 = st.tabs(["📐 Kalkulator Dinamik & Sudut", "📚 Buku Nota & Formula Sheet"])

with tab1:
    st.header("Konfigurasi Span, Beban Dinamik & Sudut (Angle)")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("1. Geometri Span Rasuk")
        length_ab = st.number_input("Panjang Total Rasuk (m)", value=12.0, step=0.5)
        e_modulus = st.number_input("Modulus Keanjalan, E (kN/mm²)", value=200.0, step=10.0)
        i_inertia = st.number_input("Momen Inersia, I (10⁶ mm⁴)", value=100.0, step=10.0)
        
        st.subheader("2. Tetapan Beban & Sudut")
        num_loads = st.number_input("Bilangan Titik Beban Berasingan", min_value=1, max_value=5, value=2, step=1)
        
        load_positions = []
        load_values = []
        load_angles = []
        load_types = []
        
        for i in range(int(num_loads)):
            st.markdown(f"**Beban ke-{i+1}**")
            pos = st.number_input(f"Jarak dari A (m) [Beban {i+1}]", value=4.0 + i*4.0, key=f"pos_{i}")
            val = st.number_input(f"Magnitud Daya (kN) [Beban {i+1}]", value=30.0, key=f"val_{i}")
            angle = st.number_input(f"Sudut / Angle dari horizontal (°) [Beban {i+1}]", value=90.0, key=f"angle_{i}")
            l_type = st.selectbox(f"Jenis Beban {i+1}", ["Point Load (Condong/Tegak)", "Concentrated Moment", "UDL Segmen"], key=f"type_{i}")
            
            load_positions.append(pos)
            load_values.append(val)
            load_angles.append(angle)
            load_types.append(l_type)

    with col_b:
        st.subheader("3. Analisis Komponen Daya & Pesongan")
        if st.button("🚀 Kira Analisis Komponen Sudut"):
            ei = (e_modulus * 1e6) * (i_inertia * 1e-6)
            st.info(f"Flexural Rigidity ($EI$) = **{ei:,.2f} kN·m²**")

            st.markdown("#### **(a) Leraian Komponen Daya ($F_x$ & $F_y$)**")
            total_fy = 0
            for idx in range(int(num_loads)):
                # Tukar darjah ke radian untuk pengiraan trigonometri
                rad = np.radians(load_angles[idx])
                fx = load_values[idx] * np.cos(rad)
                fy = load_values[idx] * np.sin(rad)
                total_fy += fy
                st.write(f"- **Beban {idx+1}**: {load_values[idx]} kN pada {load_angles[idx]}° $\rightarrow$ $F_x = {fx:.2f}$ kN, $F_y = {fy:.2f}$ kN")

            # Anggaran Pengiraan Cerun dan Pesongan berdasarkan jumlah Fy
            slope_a = (total_fy * length_ab**2) / (16 * ei)
            deflection_max = ((total_fy * length_ab**3) / (48 * ei)) * 1000

            st.markdown("#### **(b) Cerun & Pesongan Anggaran**")
            st.success(f"📌 **Anggaran Cerun di Sokongan A ($\theta_A$):** `{slope_a:.5f} \text{ rad}`")
            st.success(f"📌 **Anggaran Pesongan Maksimum:** `{deflection_max:.3f} \text{ mm}`")

    # Visualisasi Dinamik Rasuk dengan Paparan Sudut
    st.markdown("---")
    fig, ax = plt.subplots(figsize=(10, 2.5))
    ax.plot([0, length_ab], [0, 0], 'k-', lw=4, label="Rasuk Utama")
    ax.scatter([0], [0], color='red', s=100, zorder=5)
    ax.scatter([length_ab * 0.75], [0], color='green', s=100, zorder=5)
    
    for idx, pos in enumerate(load_positions):
        ax.scatter([pos], [0.2], color='blue', s=80, marker='v')
        ax.text(pos, 0.4, f'P{idx+1} ({load_angles[idx]}°)', fontsize=9, ha='center', color='blue')

    ax.text(0, -0.3, 'A', fontsize=12, fontweight='bold', ha='center')
    ax.text(length_ab * 0.75, -0.3, 'B', fontsize=12, fontweight='bold', ha='center')
    ax.set_xlim(-1, length_ab + 1)
    ax.set_ylim(-1, 2)
    ax.axis('off')
    st.pyplot(fig)

with tab2:
    st.markdown("### 📚 Appendix 1: Table for Formula Sheet & Trigonometry")
    st.markdown("Rujukan rumus leraian daya condong:")
    st.latex(r"F_x = F \cdot \cos(\theta), \quad F_y = F \cdot \sin(\theta)")
    st.latex(r"1 \cdot \Delta = \int_0^L \frac{Mm}{EI} dx")
