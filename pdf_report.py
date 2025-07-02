import os
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from ekman_calculations import EkmanTransportCalculator

# 폰트 등록
FONT_PATH = os.path.join(os.path.dirname(__file__), 'static', 'fonts')

def register_fonts():
    """앱에서 사용하는 폰트들을 등록합니다."""
    try:
        # 기본 폰트들 등록
        noto_sans_path = os.path.join(FONT_PATH, 'NotoSans-Regular.ttf')
        if os.path.exists(noto_sans_path):
            pdfmetrics.registerFont(TTFont('NotoSans', noto_sans_path))
            pdfmetrics.registerFontFamily('NotoSans', normal='NotoSans', bold='NotoSans', italic='NotoSans', boldItalic='NotoSans')
        
        # CJK 폰트들 등록
        cjk_fonts = {
            'NotoSansCJKkr': 'NotoSansCJKkr-Regular.otf',
            'NotoSansCJKjp': 'NotoSansCJKjp-Regular.otf', 
            'NotoSansCJKsc': 'NotoSansCJKsc-Regular.otf'
        }
        
        for font_name, font_file in cjk_fonts.items():
            font_path = os.path.join(FONT_PATH, font_file)
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                # 해당 폰트 패밀리에 normal, bold, italic, boldItalic을 모두 동일 폰트로 지정
                pdfmetrics.registerFontFamily(font_name, normal=font_name, bold=font_name, italic=font_name, boldItalic=font_name)
                
    except Exception as e:
        print(f"폰트 등록 중 오류: {e}")

def get_font_for_language(language):
    """언어에 따른 적절한 폰트를 반환합니다."""
    font_mapping = {
        'ko': 'NotoSansCJKkr',
        'ja': 'NotoSansCJKjp', 
        'zh': 'NotoSansCJKsc',
        'en': 'NotoSans',
        'es': 'NotoSans',
        'ru': 'NotoSans'
    }
    return font_mapping.get(language, 'NotoSans')

def get_summary_text(language, parameters, results):
    """언어별 요약 텍스트를 반환합니다."""
    summary_texts = {
        'ko': f"""
        이 보고서는 에크만 수송 계산 결과를 보여줍니다. 
        바람 속도 {parameters['wind_speed']:.1f} m/s, 
        위도 {parameters['latitude']:.1f}°에서의 계산 결과입니다.
        
        주요 결과:
        • 에크만 깊이: {results['ekman_depth']:.1f} m
        • 총 수송량: {results.get('total_transport', 0):.2e} m³/s
        • 에너지 전달률: {results['energy_transfer_rate'] * 1000:.3f} mW/m²
        """,
        'en': f"""
        This report shows the results of Ekman transport calculations.
        Calculations were performed for wind speed {parameters['wind_speed']:.1f} m/s,
        at latitude {parameters['latitude']:.1f}°.
        
        Key Results:
        • Ekman Depth: {results['ekman_depth']:.1f} m
        • Total Transport: {results.get('total_transport', 0):.2e} m³/s
        • Energy Transfer Rate: {results['energy_transfer_rate'] * 1000:.3f} mW/m²
        """,
        'zh': f"""
        本报告显示了埃克曼输运计算结果。
        计算条件：风速 {parameters['wind_speed']:.1f} m/s，
        纬度 {parameters['latitude']:.1f}°。
        
        主要结果：
        • 埃克曼深度：{results['ekman_depth']:.1f} m
        • 总输运量：{results.get('total_transport', 0):.2e} m³/s
        • 能量传输率：{results['energy_transfer_rate'] * 1000:.3f} mW/m²
        """,
        'ja': f"""
        このレポートはエクマン輸送の計算結果を示しています。
        風速 {parameters['wind_speed']:.1f} m/s、
        緯度 {parameters['latitude']:.1f}°での計算結果です。
        
        主要な結果：
        • エクマン深度：{results['ekman_depth']:.1f} m
        • 総輸送量：{results.get('total_transport', 0):.2e} m³/s
        • エネルギー伝達率：{results['energy_transfer_rate'] * 1000:.3f} mW/m²
        """,
        'es': f"""
        Este reporte muestra los resultados de los cálculos de transporte de Ekman.
        Los cálculos se realizaron para una velocidad del viento de {parameters['wind_speed']:.1f} m/s,
        a una latitud de {parameters['latitude']:.1f}°.
        
        Resultados Principales:
        • Profundidad de Ekman: {results['ekman_depth']:.1f} m
        • Transporte Total: {results.get('total_transport', 0):.2e} m³/s
        • Tasa de Transferencia de Energía: {results['energy_transfer_rate'] * 1000:.3f} mW/m²
        """,
        'ru': f"""
        Этот отчет показывает результаты расчетов экмановского переноса.
        Расчеты выполнены для скорости ветра {parameters['wind_speed']:.1f} м/с,
        на широте {parameters['latitude']:.1f}°.
        
        Ключевые результаты:
        • Экмановская глубина: {results['ekman_depth']:.1f} м
        • Общий перенос: {results.get('total_transport', 0):.2e} м³/с
        • Скорость передачи энергии: {results['energy_transfer_rate'] * 1000:.3f} мВт/м²
        """
    }
    return summary_texts.get(language, summary_texts['en'])

def create_pdf_report(results, parameters, language, translations, output_path):
    """PDF 보고서를 생성합니다."""
    register_fonts()
    
    # 언어별 폰트 설정
    font_name = get_font_for_language(language)
    t = translations[language]
    
    # 스타일 설정
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        fontName=font_name,
        fontSize=18,
        leading=22,
        spaceAfter=30,
        alignment=1  # 중앙 정렬
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        fontName=font_name,
        fontSize=14,
        leading=18,
        spaceAfter=12,
        spaceBefore=20
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        fontName=font_name,
        fontSize=10,
        leading=12,
        spaceAfter=6
    )
    
    # PDF 문서 생성
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    story = []
    
    # 제목
    story.append(Paragraph(t['pdf_title'], title_style))
    story.append(Spacer(1, 20))
    
    # 생성 날짜
    story.append(Paragraph(f"{t['pdf_generated']} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    story.append(Spacer(1, 20))
    
    # 입력 파라미터 섹션
    story.append(Paragraph(t['pdf_parameters'], heading_style))
    
    # 파라미터 테이블
    param_data = [
        [t['wind_speed'], f"{parameters['wind_speed']:.1f} m/s"],
        [t['wind_direction'], f"{parameters['wind_direction']:.0f}°"],
        [t['latitude'], f"{parameters['latitude']:.1f}°"],
        [t['depth'], f"{parameters['depth']:.0f} m"],
        [t['pdf_visualization'], parameters['vis_type'].upper()],
    ]
    
    # 위치 정보 추가
    if parameters.get('location'):
        param_data.append([t['pdf_location'], parameters['location']])
    
    param_table = Table(param_data, colWidths=[2*inch, 2*inch])
    param_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(param_table)
    story.append(Spacer(1, 20))
    
    # 계산 결과 섹션
    story.append(Paragraph(t['pdf_results'], heading_style))
    
    # 결과 테이블
    result_data = [
        [t['wind_stress'], f"{results['wind_stress'] * 1000:.2f} mN/m²"],
        [t['ekman_depth'], f"{results['ekman_depth']:.1f} m"],
        [t['total_transport'], f"{results.get('total_transport', 0):.2e} m³/s"],
        [t['energy_transfer'], f"{results['energy_transfer_rate'] * 1000:.3f} mW/m²"],
    ]
    
    result_table = Table(result_data, colWidths=[2*inch, 2*inch])
    result_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(result_table)
    story.append(Spacer(1, 20))
    
    # --- 시각화 섹션 ---
    calculator = EkmanTransportCalculator()
    vis_title = t.get('pdf_visualization', 'Visualization')
    story.append(Paragraph(vis_title, heading_style))

    # 3D 그래프 추가
    try:
        fig_3d = Figure(figsize=(8, 6), dpi=200)
        calculator._create_matplotlib_3d(fig_3d, results, language)
        fig_3d.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.9, wspace=0.4, hspace=0.4)
        
        img_buffer_3d = io.BytesIO()
        fig_3d.savefig(img_buffer_3d, format='png', bbox_inches='tight')
        img_buffer_3d.seek(0)
        
        story.append(Image(img_buffer_3d, width=6*inch, height=4*inch))
        story.append(Spacer(1, 20))
    except Exception:
        pass  # 오류 발생 시 해당 그래프는 생략

    # 2D 그래프 추가
    try:
        fig_2d = Figure(figsize=(8, 6), dpi=200)
        calculator._create_matplotlib_2d(fig_2d, results, language)
        fig_2d.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.9, wspace=0.4, hspace=0.4)

        img_buffer_2d = io.BytesIO()
        fig_2d.savefig(img_buffer_2d, format='png', bbox_inches='tight')
        img_buffer_2d.seek(0)

        story.append(Image(img_buffer_2d, width=6*inch, height=4*inch))
        story.append(Spacer(1, 20))
    except Exception:
        pass  # 오류 발생 시 해당 그래프는 생략

    # 요약 섹션
    story.append(Paragraph(t['pdf_summary'], heading_style))
    
    # 언어별 요약 텍스트
    summary_text = get_summary_text(language, parameters, results)
    story.append(Paragraph(summary_text, normal_style))
    
    # PDF 생성
    doc.build(story)
    return output_path

def save_plot_as_image(fig, output_path):
    """matplotlib 그래프를 이미지로 저장합니다."""
    fig.savefig(output_path, dpi=300, bbox_inches='tight', format='png')
    return output_path 