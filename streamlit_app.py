import plotly.graph_objects as go
import streamlit as st
import cv2
import numpy as np
from PIL import Image


st.title("Aurora Tabanlı GNSS Risk Analizi")


secim = st.radio(
    "Aurora gözlem türünü seçiniz:",
    ["Görsel yükle", "Manuel giriş"]
)


# ===============================
# ORTAK FONKSİYONLAR
# ===============================

def academic_interpretation(risk_level):

    if risk_level == 'HIGH':
        return (
            "Aurora gözlemi yüksek jeomanyetik aktiviteye işaret etmektedir. "
            "Bu koşullar altında GNSS doğruluğunda bozulma, HF iletişim kesintileri "
            "ve bilimsel ölçümlerde hata olasılığı artar."
        )

    elif risk_level == 'MODERATE':
        return (
            "Aurora gözlemi orta düzey uzay havası aktivitesini göstermektedir. "
            "GNSS sinyallerinde küçük sapmalar ve sınırlı iletişim etkileri oluşabilir."
        )

    else:
        return (
            "Aurora gözlemi düşük uzay havası aktivitesine işaret etmektedir. "
            "Operasyonel sistemler için önemli bir risk beklenmemektedir."
        )


# ===============================
# GÖRSEL MOD
# ===============================

if secim == "Görsel yükle":

    st.subheader("Görsel destekli risk analizi")

    def aurora_risk_model(brightness, color_variety, spatial_extent):

        score = 0

        score += {'low':1, 'medium':2, 'high':3}[brightness]
        score += {'single':1, 'multiple':2}[color_variety]
        score += {'narrow':1, 'wide':3}[spatial_extent]

        if score >= 7:
            return 'HIGH', score, [
                'GNSS sinyal doğruluğunda belirgin bozulmalar oluşabilir',
                'Yüksek frekanslı (HF) haberleşme sistemlerinde kesintiler meydana gelebilir',
                'Bilimsel ölçüm ve veri toplama süreçlerinde belirsizlik artabilir'
            ]
        elif score >= 5:
            return 'MODERATE', score, [
                'GNSS konum doğruluğunda sınırlı sapmalar oluşabilir',
                'Haberleşme sistemlerinde geçici etkiler gözlenebilir'
            ]
        else:
            return 'LOW', score, [
                'Önemli bir operasyonel risk beklenmemektedir'
            ]

    def extract_features(img):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        mean_brightness = np.mean(gray)

        brightness = (
            'low' if mean_brightness < 80
            else 'medium' if mean_brightness < 150
            else 'high'
        )

        color_std = np.mean([
            np.std(rgb[:,:,0]),
            np.std(rgb[:,:,1]),
            np.std(rgb[:,:,2])
        ])

        color_variety = 'multiple' if color_std > 40 else 'single'

        _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

        ratio = np.sum(thresh > 0) / thresh.size

        spatial_extent = 'wide' if ratio > 0.10 else 'narrow'

        return brightness, color_variety, spatial_extent


    def analyze_images(images):

        scores = []
        levels = []
        last_impacts = []

        for img in images:

            b, c, s = extract_features(img)

            level, score, impacts = aurora_risk_model(b, c, s)

            scores.append(score)
            levels.append(level)
            last_impacts = impacts

        avg_score = np.mean(scores)

        if avg_score >= 7:
            final_risk = 'HIGH'

        elif avg_score >= 5:
            final_risk = 'MODERATE'

        else:
            final_risk = 'LOW'

        return scores, levels, avg_score, final_risk, last_impacts


    uploaded_files = st.file_uploader(
        "Aurora görselleri yükle",
        accept_multiple_files=True
    )


    if st.button("Risk Analizi Başlat"):

        if uploaded_files:

            images = []

            for file in uploaded_files:

                image = Image.open(file)
                img = np.array(image)

                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                images.append(img)

            scores, levels, avg_score, final_risk, impacts = analyze_images(images)

            comment = academic_interpretation(final_risk)

            st.write("### SONUÇ")

            st.write("Risk Seviyesi:", final_risk)
            st.write("Ortalama Skor:", round(avg_score,2))

            st.write("Olası Etkiler:")
            for e in impacts:
                st.write("-", e)

            st.write("Yorum:")
            st.write(comment)

        # ----- GAUGE GRAFİĞİ -----

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,   
                title={'text': "GNSS Risk Skoru"},
                gauge={
                    'axis': {'range': [0, 12]},
                    'bar': {'color': "red"},
                    'steps': [    
                        {'range': [0, 5], 'color': "green"},
                        {'range': [5, 8], 'color': "orange"},
                        {'range': [8, 12], 'color': "red"},
                    ],
                }
            ))

            st.plotly_chart(fig)

# ===============================
# MANUEL MOD
# ===============================

if secim == "Manuel giriş":

    st.subheader("Manuel (kural tabanlı) risk analizi")


    def aurora_risk_model(brightness, color_variety, spatial_extent, temporal_behavior):

        risk_score = 0


        if brightness == 'yüksek':
            risk_score += 3
        elif brightness == 'orta':
            risk_score += 2
        else:
            risk_score += 1


        if color_variety == 'çok renkli':
            risk_score += 2
        else:
            risk_score += 1


        if spatial_extent == 'geniş':
            risk_score += 3
        else:
            risk_score += 1


        if temporal_behavior == 'patlama':
            risk_score += 3
        elif temporal_behavior == 'değişken':
            risk_score += 2
        else:
            risk_score += 1


        if risk_score >= 9:

            return 'HIGH', risk_score, [
                'GNSS sinyal doğruluğunda belirgin bozulmalar oluşabilir',
                'Yüksek frekanslı (HF) haberleşme sistemlerinde kesintiler meydana gelebilir',
                'Bilimsel ölçüm ve veri toplama süreçlerinde belirsizlik artabilir'
            ]

        elif risk_score >= 6:

            return 'MODERATE', risk_score, [
                'GNSS konum doğruluğunda sınırlı sapmalar oluşabilir',
                'Haberleşme sistemlerinde geçici etkiler gözlenebilir'
            ]

        else:

            return 'LOW', risk_score, [
                'Önemli bir operasyonel risk beklenmemektedir'
            ]

    brightness = st.selectbox(
        "Parlaklık",
        ['düşük','orta','yüksek']
    )

    color = st.selectbox(
        "Renk",
        ['tek renk','çok renkli']
    )

    extent = st.selectbox(
        "Yayılım",
        ['dar','geniş']
    )

    temporal = st.selectbox(
        "Zamansal davranış",
        ['sakin','değişken','patlama']
    )


    if st.button("Risk hesapla"):

        risk, score, impacts = aurora_risk_model(
            brightness,
            color,
            extent,
            temporal
        )

        comment = academic_interpretation(risk)

        st.write("### SONUÇ")

        st.write("Risk Seviyesi:", risk)
        st.write("Risk Skoru:", score)

        st.write("Olası Etkiler:")
        for e in impacts:
            st.write("-", e)

        st.write("Yorum:")
        st.write(comment)
    # ----- GAUGE GRAFİĞİ -----

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={'text': "GNSS Risk Skoru"},
            gauge={
                'axis': {'range': [0, 12]},
                'bar': {'color': "red"},
                'steps': [
                    {'range': [0, 5], 'color': "green"},
                    {'range': [5, 8], 'color': "orange"},
                    {'range': [8, 12], 'color': "red"},
                ],
            }
        ))

        st.plotly_chart(fig)
