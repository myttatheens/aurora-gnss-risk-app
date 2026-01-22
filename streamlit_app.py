import streamlit as st
import cv2
import numpy as np

st.title("Aurora Tabanlı GNSS Risk Analizi")

# ---------------- SEÇİM ----------------
secim = st.radio(
    "Aurora gözlem türünü seçiniz:",
    [
        "Görsel yükle (fotoğraf ile analiz)",
        "Manuel giriş (kural ve veri tabanlı model)"
    ]
)

# =========================================================
# =================== GÖRSEL MOD ==========================
# =========================================================
if "Görsel" in secim:
    st.subheader("Görsel Destekli Risk Analizi")

    # --- Risk Model ---
    def aurora_risk_model(brightness, color_variety, spatial_extent):
        score = 0
        score += {'low':1, 'medium':2, 'high':3}[brightness]
        score += {'single':1, 'multiple':2}[color_variety]
        score += {'narrow':1, 'wide':3}[spatial_extent]

        if score >= 7:
            return 'HIGH', score
        elif score >= 5:
            return 'MODERATE', score
        else:
            return 'LOW', score

    # --- Feature Extraction ---
    def extract_features(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        mean_brightness = np.mean(gray)
        brightness = 'low' if mean_brightness < 80 else 'medium' if mean_brightness < 150 else 'high'

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

    # --- Analyze Multiple Images ---
    def analyze_images(images):
        scores = []
        levels = []

        for img in images:
            b, c, s = extract_features(img)
            level, score = aurora_risk_model(b, c, s)
            scores.append(score)
            levels.append(level)

        avg_score = np.mean(scores)

        if avg_score >= 7:
            final_risk = 'HIGH'
        elif avg_score >= 5:
            final_risk = 'MODERATE'
        else:
            final_risk = 'LOW'

        return scores, levels, avg_score, final_risk

    uploaded_files = st.file_uploader(
        "Aurora görsellerini yükleyin",
        type=["jpg", "png", "jpeg"],
        accept_multiple_files=True
    )

    if uploaded_files and st.button("Risk Analizi Başlat"):
        images = []
        for file in uploaded_files:
            data = np.frombuffer(file.read(), np.uint8)
            img = cv2.imdecode(data, cv2.IMREAD_COLOR)
            images.append(img)

        scores, levels, avg_score, final_risk = analyze_images(images)

        st.write("Görsel Bazlı Risk Skorları:", scores)
        st.write("Görsel Bazlı Risk Seviyeleri:", levels)
        st.write("Ortalama Risk Skoru:", round(avg_score, 2))
        st.success(f"SONUÇ: {final_risk} RİSK")

# =========================================================
# =================== MANUEL MOD ==========================
# =========================================================
elif "Manuel" in secim:
    st.subheader("Manuel (Kural ve Veri Tabanlı) Risk Analizi")

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
                'GNSS signal degradation likely',
                'HF communication disruption possible',
                'Scientific measurements may be unreliable'
            ]
        elif risk_score >= 6:
            return 'MODERATE', risk_score, [
                'Minor GNSS inaccuracies possible',
                'Communication disturbances unlikely but possible'
            ]
        else:
            return 'LOW', risk_score, [
                'No significant operational risk expected'
            ]

    def academic_interpretation(risk_level):
        if risk_level == 'HIGH':
            return (
                "Girilen aurora gözlem özellikleri yüksek jeomanyetik aktiviteye işaret etmektedir. "
                "Bu koşullar altında GNSS ve haberleşme sistemlerinde bozulma riski yüksektir."
            )
        elif risk_level == 'MODERATE':
            return (
                "Aurora gözlemleri orta düzey uzay havası aktivitesini göstermektedir."
            )
        else:
            return (
                "Aurora gözlemleri sakin uzay havası koşullarına işaret etmektedir."
            )

    brightness = st.selectbox("Parlaklık", ["düşük", "orta", "yüksek"])
    color_variety = st.selectbox("Renk", ["tek renk", "çok renkli"])
    spatial_extent = st.selectbox("Yayılım", ["dar", "geniş"])
    temporal_behavior = st.selectbox("Zamansal Davranış", ["sakin", "değişken", "patlama"])

    if st.button("Risk Analizini Çalıştır"):
        risk, score, effects = aurora_risk_model(
            brightness,
            color_variety,
            spatial_extent,
            temporal_behavior
        )

        st.subheader("SONUÇ")
        st.write("Risk Seviyesi:", risk)
        st.write("Risk Skoru:", score)
        st.write("Olası Etkiler:")
        for e in effects:
            st.write("-", e)
