import tkinter as tk
from tkinter import ttk, font, messagebox, filedialog
from ekman_calculations import EkmanTransportCalculator
from translations import translations
from pdf_report import create_pdf_report
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from datetime import datetime

LOCATIONS = {
    'loc_los_angeles': {'lat': 34.0, 'wind': 3.0, 'wind_dir': 270},
    'loc_busan': {'lat': 35.1, 'wind': 3.5, 'wind_dir': 135},
    'loc_north_pacific': {'lat': 45.0, 'wind': 6.0, 'wind_dir': 135},
    'loc_north_atlantic': {'lat': 50.0, 'wind': 8.0, 'wind_dir': 270},
    'loc_okhotsk_sea': {'lat': 55.0, 'wind': 7.0, 'wind_dir': 135},
    'loc_southern_ocean': {'lat': -60.0, 'wind': 11.0, 'wind_dir': 270},
    'loc_equator': {'lat': 2.0, 'wind': 2.0, 'wind_dir': 90},
}

class EkmanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.calculator = EkmanTransportCalculator()
        self.language = tk.StringVar(value='en')
        self.language.trace_add('write', self.change_language)
        
        self.loc_name_to_key = {}
        self.current_location_key = None
        self.selected_location_var = tk.StringVar()
        
        self.wind_speed_var = tk.DoubleVar(value=10)
        self.latitude_var = tk.DoubleVar(value=30)
        self.depth_var = tk.DoubleVar(value=100)
        self.wind_direction_var = tk.DoubleVar(value=0)
        self.vis_type = tk.StringVar(value="3d")
        
        # 현재 계산 결과 저장
        self.current_results = None

        self.setup_ui()
        self._update_slider_labels()
        self.update_plot()

    def setup_ui(self):
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 제어 프레임
        self.control_frame = ttk.LabelFrame(self.main_frame, padding="10")
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # 언어 선택
        self.lang_label = ttk.Label(self.control_frame)
        self.lang_label.pack(pady=5)
        lang_map = {'en': 'English', 'ko': '한국어', 'zh': '中文', 'ja': '日本語', 'es': 'Español', 'ru': 'Русский'}
        self.lang_combo = ttk.Combobox(self.control_frame, values=list(lang_map.values()), state='readonly')
        self.lang_combo.pack()
        self.lang_combo.set(lang_map[self.language.get()])
        
        def on_lang_select(event):
            selected_lang_name = self.lang_combo.get()
            for code, name in lang_map.items():
                if name == selected_lang_name:
                    self.language.set(code)
                    break
        self.lang_combo.bind('<<ComboboxSelected>>', on_lang_select)

        # 슬라이더 및 값 표시 라벨
        self.ws_label = ttk.Label(self.control_frame)
        self.ws_label.pack(pady=5)
        ttk.Scale(self.control_frame, from_=0, to=30, orient=tk.HORIZONTAL, variable=self.wind_speed_var, length=200, command=self.handle_manual_change).pack()
        self.wind_speed_label = tk.StringVar()
        ttk.Label(self.control_frame, textvariable=self.wind_speed_label).pack()
        
        self.wd_label = ttk.Label(self.control_frame)
        self.wd_label.pack(pady=5)
        ttk.Scale(self.control_frame, from_=0, to=360, orient=tk.HORIZONTAL, variable=self.wind_direction_var, length=200, command=self.handle_manual_change).pack()
        self.wind_direction_label = tk.StringVar()
        ttk.Label(self.control_frame, textvariable=self.wind_direction_label).pack()

        self.lat_label = ttk.Label(self.control_frame)
        self.lat_label.pack(pady=5)
        ttk.Scale(self.control_frame, from_=-90, to=90, orient=tk.HORIZONTAL, variable=self.latitude_var, length=200, command=self.handle_manual_change).pack()
        self.latitude_label = tk.StringVar()
        ttk.Label(self.control_frame, textvariable=self.latitude_label).pack()

        self.depth_label_widget = ttk.Label(self.control_frame)
        self.depth_label_widget.pack(pady=5)
        self.depth_slider = ttk.Scale(self.control_frame, from_=10, to=500, orient=tk.HORIZONTAL, variable=self.depth_var, length=200, command=self.handle_manual_change)
        self.depth_slider.pack()

        self.depth_label = tk.StringVar()
        ttk.Label(self.control_frame, textvariable=self.depth_label).pack()
        
        # 버튼 프레임
        self.button_frame = ttk.Frame(self.control_frame)
        self.button_frame.pack(pady=20)
        
        # 계산 버튼
        self.calc_button = ttk.Button(self.button_frame, command=self.update_plot)
        self.calc_button.pack(side=tk.LEFT, padx=5)
        
        # 내보내기 버튼
        self.export_button = ttk.Button(self.button_frame, command=self.export_file)
        self.export_button.pack(side=tk.LEFT, padx=5)

        # 시각화 타입 프레임
        self.vis_type_frame = ttk.LabelFrame(self.control_frame, padding="10")
        self.vis_type_frame.pack(fill=tk.X, pady=10)
        
        # 라디오 버튼들을 담을 내부 프레임
        radio_button_frame = ttk.Frame(self.vis_type_frame)
        radio_button_frame.pack(fill=tk.X)

        self.radio_3d = ttk.Radiobutton(radio_button_frame, variable=self.vis_type, value="3d")
        self.radio_3d.pack(side=tk.LEFT, expand=True)
        
        self.radio_2d = ttk.Radiobutton(radio_button_frame, variable=self.vis_type, value="2d")
        self.radio_2d.pack(side=tk.LEFT, expand=True)

        # 사전 설정 프레임
        self.preset_frame = ttk.LabelFrame(self.control_frame, padding="10")
        self.preset_frame.pack(fill=tk.X, pady=10)

        self.preset_normal_button = ttk.Button(self.preset_frame, command=lambda: self.set_preset('normal'))
        self.preset_normal_button.pack(side=tk.LEFT, expand=True, padx=2)
        
        self.preset_strong_wind_button = ttk.Button(self.preset_frame, command=lambda: self.set_preset('strong_wind'))
        self.preset_strong_wind_button.pack(side=tk.LEFT, expand=True, padx=2)

        self.preset_typhoon_button = ttk.Button(self.preset_frame, command=lambda: self.set_preset('typhoon'))
        self.preset_typhoon_button.pack(side=tk.LEFT, expand=True, padx=2)

        # 지역 선택 프레임
        self.location_frame = ttk.LabelFrame(self.control_frame, padding="10")
        self.loc_combo = ttk.Combobox(self.location_frame, textvariable=self.selected_location_var, state='readonly')
        self.loc_combo.pack(pady=5)
        self.loc_combo.bind('<<ComboboxSelected>>', self.on_location_select)

        # 결과 프레임
        self.results_frame = ttk.LabelFrame(self.control_frame, padding="10")
        self.result_vars = {}
        self.result_labels = {}
        result_keys = ["wind_stress", "ekman_depth", "total_transport", "energy_transfer"]
        for i, key in enumerate(result_keys):
            self.result_labels[key] = ttk.Label(self.results_frame)
            self.result_labels[key].grid(row=i, column=0, sticky=tk.W)
            self.result_vars[key] = tk.StringVar()
            ttk.Label(self.results_frame, textvariable=self.result_vars[key]).grid(row=i, column=1, sticky=tk.W)
        
        # 정의된 프레임들을 순서대로 화면에 배치
        self.location_frame.pack(fill=tk.X, pady=10)
        self.results_frame.pack(fill=tk.X, pady=10)

        # 시각화 프레임
        self.plot_frame = ttk.Frame(self.main_frame)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.change_language()

    def change_language(self, *args):
        lang = self.language.get()
        t = translations[lang]

        # UI 텍스트 업데이트
        self.title(t['app_title'])
        self.control_frame.config(text=t['param_settings'])
        self.lang_label.config(text=t['lang_select'])
        self.ws_label.config(text=t['wind_speed'])
        self.wd_label.config(text=t['wind_direction'])
        self.lat_label.config(text=t['latitude'])
        self.depth_label_widget.config(text=t['depth'])
        self.vis_type_frame.config(text=t['vis_type'])
        self.radio_3d.config(text="3D")
        self.radio_2d.config(text="2D")
        self.calc_button.config(text=t['calc_button'])
        self.export_button.config(text=t['export_button'])
        self.results_frame.config(text=t['results_title'])
        self.preset_frame.config(text=t['preset_title'])
        self.preset_normal_button.config(text=t['preset_normal'])
        self.preset_strong_wind_button.config(text=t['preset_strong_wind'])
        self.preset_typhoon_button.config(text=t['preset_typhoon'])
        self.location_frame.config(text=t['location_select'])
        
        translated_loc_names = [t[key] for key in LOCATIONS.keys()]
        custom_text = t['loc_custom']
        translated_loc_names.append(custom_text)
        
        self.loc_name_to_key = {t[key]: key for key in LOCATIONS.keys()}
        self.loc_name_to_key[custom_text] = 'custom'
        self.loc_combo['values'] = translated_loc_names

        if self.current_location_key:
             self.selected_location_var.set(t[self.current_location_key])
        elif self.selected_location_var.get() == '' or self.loc_name_to_key.get(self.selected_location_var.get()) != 'custom':
             self.selected_location_var.set('')
        else:
             self.selected_location_var.set(custom_text)

        self.result_labels["wind_stress"].config(text=t['wind_stress'])
        self.result_labels["ekman_depth"].config(text=t['ekman_depth'])
        self.result_labels["total_transport"].config(text=t['total_transport'])
        self.result_labels["energy_transfer"].config(text=t['energy_transfer'])
        
        self.update_plot()

    def _update_slider_labels(self, _=None):
        """슬라이더 값에 따라 라벨을 업데이트합니다."""
        self.wind_speed_label.set(f"{self.wind_speed_var.get():.1f} m/s")
        self.wind_direction_label.set(f"{self.wind_direction_var.get():.0f}°")
        self.latitude_label.set(f"{self.latitude_var.get():.0f}°")
        self.depth_label.set(f"{self.depth_var.get():.0f} m")

    def on_location_select(self, event=None):
        selected_loc_name = self.selected_location_var.get()
        loc_key = self.loc_name_to_key.get(selected_loc_name)
        
        if loc_key == 'custom':
            self.current_location_key = None
            return

        if loc_key:
            self.current_location_key = loc_key
            loc_data = LOCATIONS[loc_key]
            self.latitude_var.set(loc_data['lat'])
            self.wind_speed_var.set(loc_data['wind'])
            self.wind_direction_var.set(loc_data['wind_dir'])
            self._update_slider_labels()
            self.update_plot()

    def handle_manual_change(self, _=None):
        self._update_slider_labels()
        lang = self.language.get()
        t = translations[lang]
        custom_text = t['loc_custom']
        
        if self.selected_location_var.get() != custom_text:
            self.current_location_key = None
            self.selected_location_var.set(custom_text)

    def set_preset(self, preset_type):
        self.current_location_key = None
        self.selected_location_var.set('')

        if preset_type == 'normal':
            self.wind_speed_var.set(10.0)
        elif preset_type == 'strong_wind':
            self.wind_speed_var.set(20.0)
        elif preset_type == 'typhoon':
            self.wind_speed_var.set(30.0)
        
        self._update_slider_labels()
        self.update_plot()

    def update_plot(self):
        lang = self.language.get()
        t = translations[lang]

        if self.latitude_var.get() == 0:
            tk.messagebox.showwarning(t['error_title'], t['error_msg'])
            self.latitude_var.set(1)

        results = self.calculator.calculate_ekman_transport(
            wind_speed=self.wind_speed_var.get(),
            wind_direction=self.wind_direction_var.get(),
            latitude=self.latitude_var.get(),
            depth=self.depth_var.get()
        )
        
        # 현재 결과 저장
        self.current_results = results
        
        self.fig.clear()
        
        if self.vis_type.get() == '3d':
            self.calculator._create_matplotlib_3d(self.fig, results, lang)
        else:
            self.calculator._create_matplotlib_2d(self.fig, results, lang)
        
        self.fig.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.9, wspace=0.4, hspace=0.4)
        self.canvas.draw()
        
        self.update_results_display(results)

    def update_results_display(self, results):
        self.result_vars["wind_stress"].set(f"{results['wind_stress'] * 1000:.2f} mN/m²")
        self.result_vars["ekman_depth"].set(f"{results['ekman_depth']:.1f} m")
        total_transport = np.sqrt(results['Mx']**2 + results['My']**2)
        self.result_vars["total_transport"].set(f"{total_transport:.2e} m³/s")
        self.result_vars["energy_transfer"].set(f"{results['energy_transfer_rate'] * 1000:.3f} mW/m²")

    def export_file(self):
        """PDF 또는 PNG로 내보냅니다."""
        lang = self.language.get()
        t = translations[lang]

        if self.current_results is None:
            tk.messagebox.showwarning(t['error_title'], t['error_msg_calc'])
            return
        
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        default_filename = f"Ekman_Report_{current_time}"
        
        filename = filedialog.asksaveasfilename(
            initialfile=default_filename,
            defaultextension=".pdf",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ],
            title=t.get('save_file_title', 'Save File As')
        )
        
        if not filename:
            return

        try:
            # 파일 확장자에 따라 분기
            if filename.lower().endswith('.pdf'):
                parameters = {
                    'wind_speed': self.wind_speed_var.get(),
                    'wind_direction': self.wind_direction_var.get(),
                    'latitude': self.latitude_var.get(),
                    'depth': self.depth_var.get(),
                    'vis_type': self.vis_type.get()
                }
                
                if self.current_location_key:
                    parameters['location'] = t[self.current_location_key]
                else:
                    parameters['location'] = t['loc_custom']
                
                total_transport = np.sqrt(self.current_results['Mx']**2 + self.current_results['My']**2)
                results_with_total = self.current_results.copy()
                results_with_total['total_transport'] = total_transport
                
                create_pdf_report(
                    results=results_with_total,
                    parameters=parameters,
                    language=lang,
                    translations=translations,
                    output_path=filename
                )
            elif filename.lower().endswith('.png'):
                self.fig.savefig(filename, dpi=300, bbox_inches='tight', format='png')
            else:
                # 확장자가 명확하지 않은 경우, 기본으로 PDF 저장
                tk.messagebox.showwarning(t.get('error_title', 'Error'), "Unsupported file type. Please choose .pdf or .png.")
                return

            tk.messagebox.showinfo(t.get('success_title', 'Success'), t.get('file_success_message', 'File saved successfully to:\n{filename}').format(filename=filename))

        except Exception as e:
            tk.messagebox.showerror(t.get('error_title', 'Error'), t.get('file_error_message', 'An error occurred while saving the file:\n{e}').format(e=e))

if __name__ == "__main__":
    app = EkmanApp()
    app.mainloop() 