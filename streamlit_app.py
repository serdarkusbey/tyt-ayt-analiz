import streamlit as st

st.set_page_config(
    page_title="TYT-AYT Eksik Konu Analizi",
    page_icon="📚"
)

st.title("📚 TYT-AYT Eksik Konu Analizi")
st.write("Deneme sonuçlarını gir, eksik konularını keşfet!")

ders = st.selectbox(
    "Dersini seç",
    ["Matematik", "Türkçe", "Fizik", "Kimya", "Biyoloji"]
)

konu = st.text_input("Konu adı")
dogru = st.number_input("Doğru sayısı", min_value=0, step=1)
yanlis = st.number_input("Yanlış sayısı", min_value=0, step=1)

if st.button("Analiz Et"):
    toplam = dogru + yanlis

    if not konu.strip():
        st.warning("Dayı, önce konu adını yaz!")
    elif toplam == 0:
        st.warning("En az bir soru sonucu girmelisin.")
    else:
        basari = dogru / toplam * 100
        st.metric("Başarı oranı", f"%{basari:.1f}")

        if basari < 60:
            st.warning(f"{konu} konusunu tekrar değerlendirmeni öneriyorum.")
        else:
            st.success(f"{konu} konusunda şimdilik iyi ilerliyorsun!")
