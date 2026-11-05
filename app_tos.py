import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="TOS Ultimate Advanced Calculator", layout="wide")

st.title("🏗️ TOS Advanced Structural Calculator & Formula Sheet")
st.markdown("Aplikasi lengkap pengiraan Analisis Struktur (TOS): Sokongan, Momen, Fungsi Potongan Keratan, Slope, dan Deflection.")

# Tab Menu Pilihan
tab1, tab2 = st.tabs(["📐 Kalkulator & Analisis Lanjutan", "📚 Buku Nota & Formula Sheet"])

with tab1:
    st.header("Kalkulator Analisis Rasuk Menyeluruh")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("1. Parameter & Sifat Keratan Rasuk")
        length_ab = st.number_input("Panjang Span AB (m)", value=8.0, step=0.5)
        e_modulus = st.number_input("Modulus Keanjalan, E (kN/mm²)", value=200.0, step=10.0)
        i_inertia = st.number_input("Momen Inersia, I (10⁶ mm⁴)", value=100.0, step=10.0)
        
        st.subheader("2. Beban Bertindak")
        w_udl = st.number_input("UDL sepanjang AB (kN/m)", value=30.0, step=5.0)
        m_b = st.number_input("Momen di B (kNm)", value=-12.0, step=1.0)
        p_d = st.number_input("Beban Tumpu di D (kN)", value=19.62, step=1.0)
        dist_d = st.number_input("Jarak D dari B (m)", value=4.0, step=0.5)

    with col_b:
        st.subheader("3. Keputusan Analisis Penuh")
        if st.button("🚀 Jalankan Analisis Penuh"):
            # A. Kira Tindak Balas Sokongan (Reactions)
            total_udl = w_udl * length_ab
            udl_centroid = length_ab / 2.0
            total_dist_d = length_ab + dist_d

            sum_momen_lain = (total_udl * udl_centroid) - m_b + (p_d * total_dist_d)
            r_b = sum_momen_lain / length_ab
            r_a = total_udl + p_d - r_b

            st.markdown("#### **(a) Tindak Balas Sokongan (Reactions)**")
            st.latex(f"R_A = {r_a:.2f}\\text{{ kN}}, \\quad R_B = {r_b:.2f}\\text{{ kN}}")

            # B. Flexural Rigidity EI
            ei = (e_modulus * 1e6) * (i_inertia * 1e-6)
            st.info(f"Flexural Rigidity ($EI$) = **{ei:,.2f} kN·m²**")

            # C. Fungsi Potongan Keratan (Cut Section Moment Function M(x) untuk 0 < x < L)
            st.markdown("#### **(b) Fungsi Momen Lentur Keratan $M(x)$**")
            st.latex(r"M(x) = R_A \cdot x - \frac{w \cdot x^2}{2} \quad (\text{untuk segmen AB})")
            st.markdown(f"Maka persamaan keratan: **$M(x) = {r_a:.2f}x - {w_udl/2:.1f}x^2$**")

            # D. Pengiraan Anggaran Slope & Deflection di Titik Penting
            slope_a = (r_a * length_ab**2) / (3 * ei)
            deflection_mid = ((w_udl * length_ab**4) / (384 * ei)) * 1000 # anggaran titik tengah
            deflection_d = deflection_mid * 1.5

            st.markdown("#### **(c) Cerun & Pesongan pada Titik Penting**")
            st.success(f"📌 **Cerun di Sokongan A ($\theta_A$):** `{slope_a:.5f} \text{ rad}`")
            st.success(f"📌 **Pesongan di Titik Tengah / C ($\Delta_C$):** `{deflection_mid:.3f} \text{ mm}`")
            st.success(f"📌 **Pesongan di Hujung D ($\Delta_D$):** `{deflection_d:.3f} \text{ mm}`")

    # Visualisasi Rajah Rasuk
    st.markdown("---")
    fig, ax = plt.subplots(figsize=(10, 2.5))
    ax.plot([0, length_ab], [0, 0], 'k-', lw=4, label="Rasuk AB")
    ax.plot([length_ab, length_ab + dist_d], [0, 0], 'k--', lw=2)
    ax.scatter([0], [0], color='red', s=100, zorder=5, label="A (Pin)")
    ax.scatter([length_ab], [0], color='green', s=100, zorder=5, label="B (Roller)")
    ax.text(0, -0.3, 'A', fontsize=12, fontweight='bold', ha='center')
    ax.text(length_ab, -0.3, 'B', fontsize=12, fontweight='bold', ha='center')
    ax.text(length_ab + (dist_d/2), 0.3, f'Momen B = {m_b} kNm', fontsize=10, color='blue', ha='center')
    ax.text(length_ab + dist_d, -0.3, 'D', fontsize=12, fontweight='bold', ha='center')
    ax.set_xlim(-1, length_ab + dist_d + 1)
    ax.set_ylim(-1, 2)
    ax.axis('off')
    st.pyplot(fig)

with tab2:
    st.markdown("### 📚 Appendix 1: Table for Formula Sheet")
    st.markdown("Rujukan lengkap formula Analisis Struktur (TOS).")

    st.subheader("A. Double Integration Method")
    st.latex(r"\frac{d^2v}{dx^2} = \frac{M}{EI} \quad \text{atau} \quad EI\frac{d^2y}{dx^2} = M")
    st.latex(r"\theta = \frac{dv}{dx} = \int \frac{M}{EI} dx")
    st.latex(r"v = f(x) = \iint \frac{M}{EI} dx")

    st.markdown("---")
    st.subheader("B. Virtual Work Method")
    st.latex(r"1 \cdot \Delta = \int_0^L \frac{Mm}{EI} dx")
    st.latex(r"1 \cdot \theta = \int_0^L \frac{Mm}{EI} dx")

    st.markdown("---")
    st.subheader("C. Moment Area Method")
    st.latex(r"\theta_{LR} = \frac{1}{EI} \int_{x_L}^{x_R} M dx")
    st.latex(r"t_{AB} = \frac{1}{EI} \int_{x_B}^{x_R} \bar{x} M dx")

    st.markdown("---")
    st.subheader("D. Slope Deflection Method")
    st.latex(r"M_{AB} = \frac{4EI\theta_A}{L} + \frac{2EI\theta_B}{L} - \frac{6EI\Delta}{L^2} + M^F_{AB}")

    st.markdown("---")
    st.subheader("E. Moment Distribution Method")
    st.latex(r"K_{\text{pinned}} = \frac{3EI}{L}, \quad K_{\text{fixed}} = \frac{4EI}{L}")

    st.markdown("---")
    st.subheader("F. 3-Pinned Arch")
    st.latex(r"y = \frac{4hx}{L^2}(L - x)")
