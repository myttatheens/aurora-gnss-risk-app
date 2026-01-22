secim = input("""
Aurora gözlem türünü seçiniz:

1 - Görsel yükle (fotoğraf ile analiz)
2 - Manuel giriş (kural ve veri tabanlı model)

Seçiminiz (1/2): """)
if secim == "1":
    print("Görsel destekli risk analizi başlatılıyor...\n")

    # --- IMPORTS ---
    import cv2
    import numpy as np
    import ipywidgets as widgets
    from IPython.display import display, clear_output

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

        color_std = np.mean([np.std(rgb[:,:,0]), np.std(rgb[:,:,1]), np.std(rgb[:,:,2])])
        color_variety = 'multiple' if color_std > 40 else 'single'

        _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        ratio = np.sum(thresh > 0) / thresh.size
        spatial_extent = 'wide' if ratio > 0.10 else 'narrow'

        return brightness, color_variety, spatial_extent


    # --- PROCESS MULTIPLE IMAGES ---
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


    # --- UI ELEMENTS ---
    uploader = widgets.FileUpload(
        accept='image/*',
        multiple=True,
        description='Aurora Görselleri Yükle'
    )

    run_button = widgets.Button(
        description='Risk Analizi Başlat',
        button_style='primary'
    )

    output = widgets.Output()

    # --- BUTTON ACTION ---
    def on_run_clicked(b):
        with output:
            clear_output()

            if not uploader.value:
                print("No images uploaded.")
                return

            images = []
            for file in uploader.value.values():
                data = np.frombuffer(file['content'], np.uint8)
                img = cv2.imdecode(data, cv2.IMREAD_COLOR)
                images.append(img)

            scores, levels, avg_score, final_risk = analyze_images(images)

            print("Individual Image Risk Scores:", scores)
            print("Individual Risk Levels:", levels)
            print("\nAVERAGE RISK SCORE:", round(avg_score, 2))
            print("FINAL RISK LEVEL:", final_risk)

    run_button.on_click(on_run_clicked)

    # --- DISPLAY UI ---
    display(uploader, run_button, output)

if secim == "2":
    print("Manuel (kural ve veri tabanlı) risk analizi başlatılıyor...\n")

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
            risk_level = 'HIGH'
            impacts = [
                'GNSS signal degradation likely',
                'HF communication disruption possible',
                'Scientific measurements may be unreliable'
            ]
        elif risk_score >= 6:
            risk_level = 'MODERATE'
            impacts = [
                'Minor GNSS inaccuracies possible',
                'Communication disturbances unlikely but possible'
            ]
        else:
            risk_level = 'LOW'
            impacts = [
                'No significant operational risk expected'
            ]

        return risk_level, risk_score, impacts


    def academic_interpretation(risk_level):
        if risk_level == 'HIGH':
            return (
                "Girilen aurora gözlem özellikleri yüksek jeomanyetik aktiviteye işaret etmektedir. "
                "Bu koşullar altında GNSS ve haberleşme sistemlerinde bozulma riski yüksektir; "
                "bilimsel ölçümlerin belirsizliği artabilir."
            )
        elif risk_level == 'MODERATE':
            return (
                "Aurora gözlemleri orta düzey uzay havası aktivitesini göstermektedir. "
                "GNSS doğruluğunda sınırlı bozulmalar ve geçici iletişim etkileri olasıdır."
            )
        else:
            return (
                "Aurora gözlemleri sakin uzay havası koşullarına işaret etmektedir. "
                "Önemli bir operasyonel risk beklenmemektedir."
            )

    import ipywidgets as widgets
    from IPython.display import display

    brightness_widget = widgets.Dropdown(
        options=['düşük', 'orta', 'yüksek'],
        description='Parlaklık:'
    )

    color_widget = widgets.Dropdown(
        options=['tek renk', 'çok renkli'],
        description='Renk:'
    )

    spatial_widget = widgets.Dropdown(
        options=['dar', 'geniş'],
        description='Yayılım:'
    )

    temporal_widget = widgets.Dropdown(
        options=['sakin', 'değişken', 'patlama'],
        description='Zamansal:'
    )

    output = widgets.Output()

    def run_model(button):
        output.clear_output()
        with output:
            risk, score, effects = aurora_risk_model(
                brightness_widget.value,
                color_widget.value,
                spatial_widget.value,
                temporal_widget.value
            )

            comment = academic_interpretation(risk)

            print("SONUÇ")
            print("Risk Seviyesi:", risk)
            print("Risk Skoru:", score)
            print("Olası Etkiler:")
            for effect in effects:
                print("-", effect)

            print("\nDetaylı Açıklama:")
            print(comment)

    run_button = widgets.Button(description="Run Risk Assessment")
    run_button.on_click(run_model)

    display(
        brightness_widget,
        color_widget,
        spatial_widget,
        temporal_widget,
        run_button,
        output
    )
