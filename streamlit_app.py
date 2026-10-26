
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="TYT-AYT Eksik Konu Analizi",
    page_icon="📚"
)

st.title("📚 TYT-AYT Eksik Konu Analizi")
st.write("Deneme sonuçlarını gir, eksik konularını keşfet!")

if "sonuclar" not in st.session_state:
    st.session_state.sonuclar = []

st.subheader("📝 Deneme Sonucunu Ekle")

ders = st.selectbox(
    "Dersini seç",
    [
        "Türkçe", "Matematik", "Fizik",
        "Kimya", "Biyoloji", "Tarih",
        "Coğrafya", "Felsefe"
    ]
)

konu = st.text_input("Konu adı")
dogru = st.number_input("Doğru sayısı", min_value=0, step=1)
yanlis = st.number_input("Yanlış sayısı", min_value=0, step=1)

if st.button("Sonucu Ekle"):
    toplam = dogru + yanlis

    if not konu.strip():
        st.warning("Önce konu adını yaz!")
    elif toplam == 0:
        st.warning("En az bir soru sonucu girmelisin.")
    else:
        basari = dogru / toplam * 100

        st.session_state.sonuclar.append({
            "Ders": ders,
            "Konu": konu.strip(),
            "Doğru": dogru,
            "Yanlış": yanlis,
            "Başarı (%)": round(basari, 1)
        })

        st.success("Sonuç eklendi!")

if st.session_state.sonuclar:
    st.subheader("📊 Sonuçların")

    df = pd.DataFrame(st.session_state.sonuclar)
    st.dataframe(df, use_container_width=True)

    st.subheader("🎯 Tekrar Önceliğin")

    analiz = (
        df.groupby(["Ders", "Konu"], as_index=False)
        .agg({
            "Doğru": "sum",
            "Yanlış": "sum"
        })
    )

    analiz["Toplam"] = analiz["Doğru"] + analiz["Yanlış"]
    analiz["Başarı (%)"] = (
        analiz["Doğru"] / analiz["Toplam"] * 100
    ).round(1)

    analiz = analiz.sort_values("Başarı (%)")

    for _, satir in analiz.iterrows():
        st.write(
            f"**{satir['Ders']} — {satir['Konu']}**: "
            f"%{satir['Başarı (%)']} başarı"
        )

        if satir["Başarı (%)"] < 60:
            st.warning("Tekrar önceliği yüksek.")
        elif satir["Başarı (%)"] < 80:
            st.info("Biraz daha pratik yapabilirsin.")
        else:
            st.success("Şimdilik iyi gidiyorsun!")

    if st.button("Bütün sonuçları temizle"):
        st.session_state.sonuclar = []
        st.rerun()
