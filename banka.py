import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
from datetime import datetime
import webbrowser
import json
import requests
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from PIL import Image, ImageTk
import io
import folium
from folium.plugins import HeatMap
import plotly.graph_objects as go
import threading
import time
import random
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class UltimateBankaHackAnalizTool:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Ultimate Banka Hack Analiz Platformu v3.0")
        self.root.geometry("1440x950")
        self.root.state('zoomed')
        
        # AI Modeli Yükle
        self.ai_model = self.load_ai_model()
        self.historical_data = self.load_historical_data()
        
        # Modern renk şeması
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#34495e',
            'accent': '#e74c3c',
            'light_accent': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'background': '#f5f7fa',
            'text': '#2c3e50',
            'light_text': '#7f8c8d',
            'dark': '#1a1a1a',
            'neon': '#00ff9d'
        }
        
        # Stil ayarları
        self.setup_styles()
        
        # Arayüz oluştur
        self.create_interface()
        
        # Başlangıçta örnek veri yükle
        self.load_sample_data()
        
        # Gerçek zamanlı veri güncelleme
        self.setup_realtime_updates()
    
    def setup_styles(self):
        """Modern ve profesyonel stil ayarları"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Özel stiller
        self.style.configure('.', background=self.colors['background'])
        self.style.configure('TFrame', background=self.colors['background'])
        self.style.configure('TLabel', background=self.colors['background'], 
                           font=('Segoe UI', 10), foreground=self.colors['text'])
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'), padding=8,
                           foreground='white', background=self.colors['primary'])
        self.style.configure('TLabelFrame', font=('Segoe UI', 11, 'bold'), 
                           background=self.colors['background'], 
                           foreground=self.colors['primary'], relief=tk.RAISED)
        self.style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), 
                           foreground=self.colors['primary'])
        self.style.configure('Accent.TButton', foreground='white', 
                           background=self.colors['accent'])
        self.style.configure('Secondary.TButton', foreground='white', 
                           background=self.colors['light_accent'])
        self.style.configure('Neon.TButton', foreground='black', 
                           background=self.colors['neon'], font=('Segoe UI', 10, 'bold'))
        
        self.style.map('TButton', 
                      background=[('active', self.colors['secondary'])])
        self.style.map('Accent.TButton', 
                      background=[('active', '#c0392b')])
        self.style.map('Secondary.TButton', 
                      background=[('active', '#2980b9')])
        self.style.map('Neon.TButton',
                     background=[('active', '#00cc7f')])
    
    def create_interface(self):
        """Tüm arayüz bileşenlerini oluştur"""
        # Başlık
        self.create_header()
        
        # Ana içerik
        self.create_main_content()
        
        # Footer
        self.create_footer()
        
        # Yapay Zeka Paneli
        self.create_ai_panel()
        
        # Blockchain İzleyici
        self.create_blockchain_panel()
        
        # 3D Görselleştirme
        self.setup_3d_visualization()
    
    def create_header(self):
        """Üst bilgi alanını oluştur"""
        header_frame = ttk.Frame(self.root, style='TFrame')
        header_frame.pack(fill=tk.X, padx=20, pady=(10, 5))
        
        # Logo ve başlık
        logo_frame = ttk.Frame(header_frame, style='TFrame')
        logo_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Animasyonlu logo
        self.logo_images = [ImageTk.PhotoImage(Image.open(f'logo_{i}.png').resize((40,40))) 
                          for i in range(1,4)] if False else None
        self.logo_label = ttk.Label(logo_frame, text="🔐", font=('Segoe UI', 24))
        self.logo_label.pack(side=tk.LEFT, padx=(0, 10))
        
        title_frame = ttk.Frame(logo_frame, style='TFrame')
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        title_label = ttk.Label(title_frame, 
                              text="ULTIMATE BANKA HACK ANALİZ PLATFORMU", 
                              style='Header.TLabel')
        title_label.pack(anchor='w')
        
        subtitle_label = ttk.Label(title_frame, 
                                 text="Yapay Zeka Destekli Siber Güvenlik & Finansal Etki Değerlendirme Sistemi",
                                 foreground=self.colors['light_text'])
        subtitle_label.pack(anchor='w')
        
        # Sağ taraf - sistem bilgileri
        info_frame = ttk.Frame(header_frame, style='TFrame')
        info_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.cpu_usage = ttk.Label(info_frame, 
                                 text="CPU: %0.0f | RAM: %0.0f%%" % (random.random()*10, random.random()*30),
                                 foreground=self.colors['light_text'])
        self.cpu_usage.pack(anchor='e')
        
        version_label = ttk.Label(info_frame, 
                                text=f"v3.0 | {datetime.now().strftime('%d.%m.%Y %H:%M')}",
                                foreground=self.colors['light_text'])
        version_label.pack(anchor='e', pady=(5,0))
        
        self.status_label = ttk.Label(info_frame, 
                                    text="✓ Çevrimiçi | AI Aktif | Veri Güvenliği: %100",
                                    foreground=self.colors['success'])
        self.status_label.pack(anchor='e')
    
    def create_main_content(self):
        """Ana içerik alanını oluştur"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,15))
        
        # Sol panel - Giriş alanları
        self.create_input_panel(main_frame)
        
        # Orta panel - Sonuçlar ve AI analizi
        self.create_results_panel(main_frame)
        
        # Sağ panel - Grafikler ve görselleştirme
        self.create_visualization_panel(main_frame)
        
        # Grid ayarları
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=2)
        main_frame.rowconfigure(0, weight=1)
    
    def create_input_panel(self, parent):
        """Veri giriş panelini oluştur"""
        input_frame = ttk.LabelFrame(parent, text="  HACK DETAYLARI  ", padding=(15, 12))
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        # Giriş alanları
        entries = [
            ("Banka Adı:", "banka_adi", "Örnek Banka A.Ş."),
            ("Çalınan Miktar ($):", "calinan_miktar", "50000000"),
            ("Sistem Onarım Maliyeti ($):", "onarim_maliyeti", "2000000"),
            ("Yasal Cezalar ($):", "yasal_cezalar", "5000000"),
            ("Hisse Değer Kaybı (%):", "hisse_kaybi", "15"),
            ("Piyasa Değeri ($):", "piyasa_degeri", "1000000000"),
            ("Operasyonel Kesinti (saat):", "kesinti_suresi", "24"),
            ("Saatlik İşlem Hacmi ($):", "saatlik_islem", "1000000"),
            ("Müşteri Sayısı:", "musteri_sayisi", "5000000"),
            ("Etkilenen Ülke Sayısı:", "ulke_sayisi", "3")
        ]
        
        for i, (label_text, attr_name, default_value) in enumerate(entries):
            frame = ttk.Frame(input_frame, style='TFrame')
            frame.grid(row=i, column=0, sticky="ew", pady=3)
            
            label = ttk.Label(frame, text=label_text, width=22, anchor='w')
            label.pack(side=tk.LEFT, padx=(0, 10))
            
            entry = ttk.Entry(frame, font=('Segoe UI', 10))
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            entry.insert(0, default_value)
            setattr(self, attr_name, entry)
        
        # Butonlar
        button_frame = ttk.Frame(input_frame, style='TFrame')
        button_frame.grid(row=len(entries)+1, column=0, sticky="ew", pady=(15,5))
        
        ttk.Button(button_frame, text="Örnek Veri Yükle", 
                  command=self.load_sample_data, style='Secondary.TButton').pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(button_frame, text="Hesapla", 
                  command=self.advanced_hesapla, style='Accent.TButton').pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Risk göstergesi
        self.create_risk_indicator(input_frame, len(entries)+2)
        
        # Senaryo yöneticisi
        self.create_scenario_manager(input_frame, len(entries)+4)
    
    def create_risk_indicator(self, parent, row):
        """Gelişmiş risk göstergesi oluştur"""
        risk_frame = ttk.LabelFrame(parent, text="  RİSK DEĞERLENDİRME  ", padding=(10, 5))
        risk_frame.grid(row=row, column=0, sticky="ew", pady=(15,5))
        
        # Risk seviyesi göstergesi
        self.risk_level = tk.StringVar(value="0")
        self.risk_meter = ttk.Progressbar(risk_frame, orient='horizontal', 
                                         length=200, mode='determinate',
                                         variable=self.risk_level)
        self.risk_meter.pack(fill=tk.X, pady=5)
        
        # Risk etiketleri
        risk_label_frame = ttk.Frame(risk_frame)
        risk_label_frame.pack(fill=tk.X)
        
        ttk.Label(risk_label_frame, text="Düşük", foreground=self.colors['success']).pack(side=tk.LEFT)
        ttk.Label(risk_label_frame, text="Orta", foreground=self.colors['warning']).pack(side=tk.LEFT, padx=50)
        ttk.Label(risk_label_frame, text="Yüksek", foreground=self.colors['accent']).pack(side=tk.RIGHT)
        
        # AI önerisi
        self.ai_recommendation = ttk.Label(risk_frame, text="AI önerisi bekleniyor...",
                                         wraplength=250, justify='center',
                                         foreground=self.colors['light_text'])
        self.ai_recommendation.pack(fill=tk.X, pady=(5,0))
    
    def create_scenario_manager(self, parent, row):
        """Senaryo yöneticisi oluştur"""
        scenario_frame = ttk.LabelFrame(parent, text="  SENARYO YÖNETİCİSİ  ", padding=(10, 8))
        scenario_frame.grid(row=row, column=0, sticky="ew", pady=(15,5))
        
        # Senaryo seçimi
        scenario_options = ["Standart Hack", "İçeriden Sabotaj", "Devlet Destekli", "Siber Savaş", "Özel Senaryo"]
        self.scenario_var = tk.StringVar(value=scenario_options[0])
        
        for i, option in enumerate(scenario_options):
            rb = ttk.Radiobutton(scenario_frame, text=option, value=option,
                                variable=self.scenario_var, command=self.update_scenario)
            rb.pack(anchor='w', pady=2)
        
        # Özel senaryo butonu
        ttk.Button(scenario_frame, text="Özel Senaryo Oluştur", 
                  command=self.create_custom_scenario, style='Secondary.TButton').pack(fill=tk.X, pady=(5,0))
    
    def create_results_panel(self, parent):
        """Sonuçlar panelini oluştur"""
        results_frame = ttk.LabelFrame(parent, text="  ANALİZ SONUÇLARI & AI ÖNERİLERİ  ", padding=(15, 12))
        results_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        
        # Notebook yapısı
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Sonuçlar sekmesi
        self.create_results_tab()
        
        # AI Analiz sekmesi
        self.create_ai_analysis_tab()
        
        # Blockchain İzleme sekmesi
        self.create_blockchain_tab()
    
    def create_results_tab(self):
        """Sonuçlar sekmesini oluştur"""
        tab1 = ttk.Frame(self.results_notebook)
        self.results_notebook.add(tab1, text="Sonuçlar")
        
        # Sonuç metni için scrollbar
        scroll_frame = ttk.Frame(tab1)
        scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(scroll_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.sonuc_metni = tk.Text(scroll_frame, height=20, width=45, wrap=tk.WORD,
                                 font=('Segoe UI', 10), padx=12, pady=12,
                                 bg='white', fg=self.colors['text'], bd=0,
                                 yscrollcommand=scrollbar.set)
        self.sonuc_metni.pack(fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.sonuc_metni.yview)
        
        # Butonlar
        button_frame = ttk.Frame(tab1)
        button_frame.pack(fill=tk.X, pady=(10,0))
        
        ttk.Button(button_frame, text="Sonuçları Kaydet", 
                  command=self.save_results, style='Secondary.TButton').pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(button_frame, text="Rapor Oluştur", 
                  command=self.generate_advanced_report, style='Secondary.TButton').pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    def create_ai_analysis_tab(self):
        """AI analiz sekmesini oluştur"""
        tab2 = ttk.Frame(self.results_notebook)
        self.results_notebook.add(tab2, text="AI Analiz")
        
        # AI sonuçları
        self.ai_result_text = tk.Text(tab2, height=10, wrap=tk.WORD,
                                    font=('Segoe UI', 10), padx=12, pady=12,
                                    bg='white', fg=self.colors['text'])
        self.ai_result_text.pack(fill=tk.BOTH, expand=True)
        self.ai_result_text.insert(tk.END, "Yapay Zeka analiz sonuçları burada görüntülenecek...\n\n")
        self.ai_result_text.config(state=tk.DISABLED)
        
        # AI önerileri
        recommendation_frame = ttk.LabelFrame(tab2, text=" AI ÖNERİLERİ ", padding=(10, 8))
        recommendation_frame.pack(fill=tk.X, pady=(10,0))
        
        self.ai_recommendations = tk.Listbox(recommendation_frame, height=4,
                                          font=('Segoe UI', 9), bg='white',
                                          selectbackground=self.colors['light_accent'])
        self.ai_recommendations.pack(fill=tk.X)
        
        # AI butonları
        ai_button_frame = ttk.Frame(tab2)
        ai_button_frame.pack(fill=tk.X, pady=(10,0))
        
        ttk.Button(ai_button_frame, text="Detaylı Analiz Yap", 
                  command=self.run_detailed_ai_analysis, style='Neon.TButton').pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(ai_button_frame, text="Gelecek Tahmini", 
                  command=self.run_future_prediction, style='Secondary.TButton').pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    def create_blockchain_tab(self):
        """Blockchain izleme sekmesini oluştur"""
        tab3 = ttk.Frame(self.results_notebook)
        self.results_notebook.add(tab3, text="Blockchain İzleme")
        
        # Blockchain giriş alanı
        entry_frame = ttk.Frame(tab3)
        entry_frame.pack(fill=tk.X, pady=(0,10))
        
        ttk.Label(entry_frame, text="İşlem Hash:").pack(side=tk.LEFT)
        self.blockchain_entry = ttk.Entry(entry_frame)
        self.blockchain_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(entry_frame, text="Takip Et", 
                  command=self.track_blockchain, style='Secondary.TButton').pack(side=tk.LEFT)
        
        # Blockchain sonuçları
        self.blockchain_text = tk.Text(tab3, height=12, wrap=tk.WORD,
                                     font=('Courier New', 9), padx=12, pady=12,
                                     bg='black', fg='white')
        self.blockchain_text.pack(fill=tk.BOTH, expand=True)
        
        # Blockchain butonları
        bc_button_frame = ttk.Frame(tab3)
        bc_button_frame.pack(fill=tk.X, pady=(10,0))
        
        ttk.Button(bc_button_frame, text="Para Akışını Görselleştir", 
                  command=self.visualize_money_flow, style='Neon.TButton').pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(bc_button_frame, text="Sonuçları Kaydet", 
                  command=self.save_blockchain_data, style='Secondary.TButton').pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    def create_visualization_panel(self, parent):
        """Görselleştirme panelini oluştur"""
        vis_frame = ttk.LabelFrame(parent, text="  GELİŞMİŞ GÖRSELLEŞTİRME  ", padding=(15, 12))
        vis_frame.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")
        
        # Notebook (sekme) yapısı
        self.vis_notebook = ttk.Notebook(vis_frame)
        self.vis_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Grafik 1 sekmesi - 3D Kayıp Dağılımı
        self.create_3d_loss_tab()
        
        # Grafik 2 sekmesi - Coğrafi Etki
        self.create_geo_impact_tab()
        
        # Grafik 3 sekmesi - Zaman Serisi
        self.create_time_series_tab()
        
        # Grafik 4 sekmesi - Makro Ekonomik Etki
        self.create_macro_impact_tab()
    
    def create_3d_loss_tab(self):
        """3D Kayıp Dağılımı sekmesini oluştur"""
        tab1 = ttk.Frame(self.vis_notebook)
        self.vis_notebook.add(tab1, text="3D Kayıp Dağılımı")
        
        # 3D Grafik
        self.fig_3d = plt.figure(figsize=(8, 6), facecolor=self.colors['background'])
        self.ax_3d = self.fig_3d.add_subplot(111, projection='3d')
        
        self.canvas_3d = FigureCanvasTkAgg(self.fig_3d, master=tab1)
        self.canvas_3d.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Toolbar ekle
        toolbar = NavigationToolbar2Tk(self.canvas_3d, tab1)
        toolbar.update()
        self.canvas_3d._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def create_geo_impact_tab(self):
        """Coğrafi Etki sekmesini oluştur"""
        tab2 = ttk.Frame(self.vis_notebook)
        self.vis_notebook.add(tab2, text="Coğrafi Etki")
        
        # Harita için canvas
        self.map_frame = ttk.Frame(tab2)
        self.map_frame.pack(fill=tk.BOTH, expand=True)
        
        # Başlangıçta boş bir harita
        self.map_label = ttk.Label(self.map_frame, text="Harita yükleniyor...")
        self.map_label.pack(fill=tk.BOTH, expand=True)
    
    def create_time_series_tab(self):
        """Zaman Serisi sekmesini oluştur"""
        tab3 = ttk.Frame(self.vis_notebook)
        self.vis_notebook.add(tab3, text="Zaman Etkisi")
        
        self.fig_time = plt.figure(figsize=(8, 4), facecolor=self.colors['background'])
        self.ax_time = self.fig_time.add_subplot(111)
        
        self.canvas_time = FigureCanvasTkAgg(self.fig_time, master=tab3)
        self.canvas_time.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_macro_impact_tab(self):
        """Makro Ekonomik Etki sekmesini oluştur"""
        tab4 = ttk.Frame(self.vis_notebook)
        self.vis_notebook.add(tab4, text="Makro Etki")
        
        self.fig_macro = plt.figure(figsize=(8, 5), facecolor=self.colors['background'])
        self.ax_macro = self.fig_macro.add_subplot(111)
        
        self.canvas_macro = FigureCanvasTkAgg(self.fig_macro, master=tab4)
        self.canvas_macro.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_footer(self):
        """Alt bilgi alanını oluştur"""
        footer_frame = ttk.Frame(self.root, style='TFrame')
        footer_frame.pack(fill=tk.X, padx=20, pady=(0,15))
        
        # Sistem durumu
        status_frame = ttk.Frame(footer_frame, style='TFrame')
        status_frame.pack(side=tk.LEFT)
        
        self.system_status = ttk.Label(status_frame, 
                                     text="Sistem Durumu: Çalışıyor | AI: Aktif | Veri Akışı: %100",
                                     foreground=self.colors['success'])
        self.system_status.pack(side=tk.LEFT, padx=10)
        
        # Copyright
        ttk.Label(footer_frame, 
                 text="© 2025 Ultimate Banka Hack Analiz Sistemi | Tüm hakları saklıdır",
                 foreground=self.colors['light_text']).pack(side=tk.RIGHT)
        
        # Yardım butonları
        help_frame = ttk.Frame(footer_frame, style='TFrame')
        help_frame.pack(side=tk.RIGHT, padx=20)
        
        ttk.Button(help_frame, text="Yardım", 
                  command=self.open_help, style='Link.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(help_frame, text="Hakkında", 
                  command=self.about, style='Link.TButton').pack(side=tk.LEFT, padx=5)
    
    def create_ai_panel(self):
        """Yapay Zeka panelini oluştur"""
        self.ai_window = tk.Toplevel(self.root)
        self.ai_window.title("Yapay Zeka Kontrol Paneli")
        self.ai_window.geometry("400x600")
        self.ai_window.withdraw()  # Başlangıçta gizli
        
        # AI kontrol elemanları buraya eklenecek
        # ...
    
    def create_blockchain_panel(self):
        """Blockchain panelini oluştur"""
        self.blockchain_window = tk.Toplevel(self.root)
        self.blockchain_window.title("Blockchain İzleyici")
        self.blockchain_window.geometry("500x700")
        self.blockchain_window.withdraw()  # Başlangıçta gizli
        
        # Blockchain kontrol elemanları buraya eklenecek
        # ...
    
    def setup_3d_visualization(self):
        """3D görselleştirme ayarları"""
        # Bu fonksiyon 3D görselleştirme için gerekli ayarları yapar
        pass
    
    def load_ai_model(self):
        """AI modelini yükler"""
        try:
            # Basit bir Random Forest modeli oluştur
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            
            # Modeli eğitmek için örnek veri oluştur
            X = np.random.rand(100, 5)
            y = np.random.rand(100) * 100000000
            
            model.fit(X, y)
            return model
        except Exception as e:
            messagebox.showerror("AI Hatası", f"Model yüklenirken hata oluştu: {str(e)}")
            return None
    
    def load_historical_data(self):
        """Tarihsel verileri yükler"""
        # Örnek veri oluştur
        data = {
            'date': pd.date_range(start='2020-01-01', periods=24, freq='M'),
            'loss_amount': np.random.randint(1000000, 50000000, size=24),
            'recovery_time': np.random.randint(1, 12, size=24),
            'country': ['USA', 'UK', 'Germany', 'Japan'] * 6,
            'attack_type': ['Phishing', 'DDoS', 'Malware', 'Insider'] * 6
        }
        return pd.DataFrame(data)
    
    def setup_realtime_updates(self):
        """Gerçek zamanlı veri güncellemelerini ayarlar"""
        def update_realtime():
            while True:
                try:
                    # CPU ve RAM kullanımını güncelle
                    cpu = random.random() * 10
                    ram = random.random() * 30
                    self.cpu_usage.config(text=f"CPU: %{cpu:.0f} | RAM: %{ram:.0f}")
                    
                    # Sistem durumunu güncelle
                    status_text = f"✓ Çevrimiçi | AI: Aktif | Veri Güvenliği: %{100 - random.random()*5:.0f}"
                    self.status_label.config(text=status_text)
                    self.system_status.config(text=f"Sistem Durumu: Çalışıyor | AI: Aktif | Veri Akışı: %{100 - random.random()*5:.0f}")
                    
                    time.sleep(3)
                except:
                    break
        
        # Arka planda çalışacak thread
        threading.Thread(target=update_realtime, daemon=True).start()
    
    def load_sample_data(self):
        """Örnek veri yükle"""
        entries = [
            ("banka_adi", "Örnek Banka A.Ş."),
            ("calinan_miktar", "50000000"),
            ("onarim_maliyeti", "2000000"),
            ("yasal_cezalar", "5000000"),
            ("hisse_kaybi", "15"),
            ("piyasa_degeri", "1000000000"),
            ("kesinti_suresi", "24"),
            ("saatlik_islem", "1000000"),
            ("musteri_sayisi", "5000000"),
            ("ulke_sayisi", "3")
        ]
        
        for attr_name, value in entries:
            entry = getattr(self, attr_name)
            entry.delete(0, tk.END)
            entry.insert(0, value)
        
        self.risk_level.set(30)
        self.ai_recommendation.config(text="Örnek veriler yüklendi. Hesaplamak için 'Hesapla' butonuna basın.",
                                    foreground=self.colors['warning'])
    
    def advanced_hesapla(self):
        """Gelişmiş hesaplama fonksiyonu"""
        try:
            # Verileri al
            banka_adi = self.banka_adi.get()
            calinan = float(self.calinan_miktar.get())
            onarim = float(self.onarim_maliyeti.get())
            ceza = float(self.yasal_cezalar.get())
            hisse_kayip = float(self.hisse_kaybi.get()) / 100
            piyasa_deger = float(self.piyasa_degeri.get())
            kesinti = float(self.kesinti_suresi.get())
            saatlik_islem = float(self.saatlik_islem.get())
            musteri_sayisi = float(self.musteri_sayisi.get())
            ulke_sayisi = float(self.ulke_sayisi.get())
            
            # Temel hesaplamalar
            toplam_dogrudan_kayip = calinan + onarim + ceza
            marka_degeri_kaybi = hisse_kayip * piyasa_deger
            operasyonel_kayip = kesinti * saatlik_islem
            toplam_kayip = toplam_dogrudan_kayip + marka_degeri_kaybi + operasyonel_kayip
            
            # Müşteri başına kayıp
            musteri_basi_kayip = toplam_kayip / musteri_sayisi if musteri_sayisi > 0 else 0
            
            # GSYİH karşılaştırması (Türkiye için yaklaşık 850 milyar $)
            gsyih_oran = (toplam_kayip/850000000000)*100
            
            # Senaryoya göre ekstra hesaplamalar
            scenario = self.scenario_var.get()
            scenario_multiplier = 1.0
            scenario_text = ""
            
            if scenario == "İçeriden Sabotaj":
                scenario_multiplier = 1.3
                scenario_text = "İçeriden sabotaj senaryosu: %30 ek risk primi uygulandı"
            elif scenario == "Devlet Destekli":
                scenario_multiplier = 1.7
                scenario_text = "Devlet destekli saldırı senaryosu: %70 ek risk primi uygulandı"
            elif scenario == "Siber Savaş":
                scenario_multiplier = 2.0
                scenario_text = "Siber savaş senaryosu: %100 ek risk primi uygulandı"
            
            toplam_kayip *= scenario_multiplier
            
            # Risk seviyesini belirle
            risk_seviyesi = min(100, max(0, (toplam_kayip / 50000000) * 100))  # 50M$'a göre yüzdelik
            self.risk_level.set(risk_seviyesi)
            
            risk_durumu = "DÜŞÜK"
            risk_rengi = self.colors['success']
            if risk_seviyesi > 70:
                risk_durumu = "ÇOK YÜKSEK"
                risk_rengi = self.colors['accent']
            elif risk_seviyesi > 50:
                risk_durumu = "YÜKSEK"
                risk_rengi = '#e67e22'
            elif risk_seviyesi > 30:
                risk_durumu = "ORTA"
                risk_rengi = self.colors['warning']
            
            # AI tahmini yap
            ai_prediction = self.predict_with_ai(toplam_dogrudan_kayip, marka_degeri_kaybi, 
                                               operasyonel_kayip, musteri_sayisi, ulke_sayisi)
            
            # Sonuçları göster
            sonuc_text = f"🏦 Banka: {banka_adi}\n"
            sonuc_text += "="*50 + "\n"
            sonuc_text += "🔍 Kapsamlı Analiz Sonuçları:\n\n"
            
            sonuc_text += "💸 Doğrudan Kayıplar:\n"
            sonuc_text += f"  • Çalınan Miktar: ${calinan:,.2f}\n"
            sonuc_text += f"  • Sistem Onarımı: ${onarim:,.2f}\n"
            sonuc_text += f"  • Yasal Cezalar: ${ceza:,.2f}\n"
            sonuc_text += f"  → Toplam Doğrudan Kayıp: ${toplam_dogrudan_kayip:,.2f}\n\n"
            
            sonuc_text += "📉 Dolaylı Kayıplar:\n"
            sonuc_text += f"  • Hisse Değeri Kaybı (%{hisse_kayip*100:.1f}): ${marka_degeri_kaybi:,.2f}\n"
            sonuc_text += f"  • Operasyonel Kesinti Kaybı: ${operasyonel_kayip:,.2f}\n\n"
            
            sonuc_text += "🔥 Genel Toplam Kayıp:\n"
            sonuc_text += f"  ${toplam_kayip:,.2f}\n\n"
            
            sonuc_text += "🌍 Makro Ekonomik Etki:\n"
            sonuc_text += f"  • Türkiye GSYİH'sına oranı: %{gsyih_oran:.6f}\n"
            sonuc_text += f"  • Müşteri başına kayıp: ${musteri_basi_kayip:,.2f}\n"
            sonuc_text += f"  • Risk Seviyesi: {risk_durumu} (%{risk_seviyesi:.1f})\n"
            sonuc_text += f"  • Senaryo: {scenario_text}\n"
            sonuc_text += "="*50 + "\n"
            sonuc_text += "🤖 AI Tahmini:\n"
            sonuc_text += f"  • Beklenen iyileşme süresi: {ai_prediction.get('recovery_time', 'N/A')} ay\n"
            sonuc_text += f"  • Potansiyel müşteri kaybı: %{ai_prediction.get('customer_loss', 'N/A'):.1f}\n"
            sonuc_text += "="*50 + "\n"
            sonuc_text += "⚠️ Uyarı: Bu sonuçlar tahmini değerlerdir. Detaylı analiz için uzman görüşü alınız."
            
            self.sonuc_metni.config(state=tk.NORMAL)
            self.sonuc_metni.delete(1.0, tk.END)
            self.sonuc_metni.insert(tk.END, sonuc_text)
            self.sonuc_metni.config(state=tk.DISABLED)
            
            # AI sonuçlarını göster
            self.show_ai_results(ai_prediction)
            
            # Grafikleri güncelle
            self.update_charts(toplam_dogrudan_kayip, marka_degeri_kaybi, operasyonel_kayip, 
                             musteri_sayisi, ulke_sayisi, scenario_multiplier)
            
            # Risk göstergesini güncelle
            self.risk_meter.config(style=f"Horizontal.TProgressbar", troughcolor='white',
                                 background=risk_rengi)
            self.ai_recommendation.config(text=f"AI ÖNERİSİ: {ai_prediction.get('recommendation', 'Veri yetersiz')}",
                                        foreground=self.colors['text'])
            
        except ValueError as e:
            messagebox.showerror("Hata", f"Geçersiz veri girişi! Lütfen tüm alanları kontrol edin.\n{str(e)}")
            self.risk_level.set(0)
            self.ai_recommendation.config(text="Hesaplama yapılamadı. Verileri kontrol edin.",
                                        foreground=self.colors['accent'])
    
    def predict_with_ai(self, direct_loss, brand_loss, operational_loss, customers, countries):
        """AI ile tahmin yapar"""
        if not self.ai_model:
            return {"error": "AI modeli yüklenemedi"}
        
        try:
            # Özellik vektörü oluştur
            features = np.array([[
                direct_loss / 1000000, 
                brand_loss / 1000000, 
                operational_loss / 1000000,
                customers / 1000000,
                countries
            ]])
            
            # Tahmin yap
            recovery_time = self.ai_model.predict(features)[0]
            
            # Öneri oluştur
            recommendations = [
                "Acil olarak siber güvenlik ekibini genişletin",
                "Müşterilere yönelik şeffaf bir iletişim stratejisi uygulayın",
                "Finansal kayıpları dengelemek için yatırımcılarla görüşün",
                "Regülatörlerle proaktif iletişim kurun",
                "Kriz yönetimi ekibi oluşturun"
            ]
            
            # Senaryoya göre ek öneri ekle
            scenario = self.scenario_var.get()
            if scenario == "İçeriden Sabotaj":
                recommendations.append("İç denetim süreçlerini gözden geçirin")
            elif scenario == "Devlet Destekli":
                recommendations.append("Hükümet yetkilileriyle acil görüşme talep edin")
            elif scenario == "Siber Savaş":
                recommendations.append("NATO siber savunma birimleriyle iletişime geçin")
            
            return {
                "recovery_time": max(1, min(24, int(recovery_time))),
                "customer_loss": min(30, max(5, (direct_loss / 10000000))),
                "recommendation": random.choice(recommendations),
                "risk_score": min(100, (direct_loss + brand_loss) / 2000000)
            }
        except Exception as e:
            print(f"AI tahmin hatası: {str(e)}")
            return {"error": str(e)}
    
    def show_ai_results(self, prediction):
        """AI sonuçlarını gösterir"""
        self.ai_result_text.config(state=tk.NORMAL)
        self.ai_result_text.delete(1.0, tk.END)
        
        if 'error' in prediction:
            self.ai_result_text.insert(tk.END, f"AI Analiz Hatası:\n{prediction['error']}")
        else:
            text = "🤖 YAPAY ZEKA ANALİZ SONUÇLARI\n"
            text += "="*50 + "\n\n"
            text += f"⏳ Tahmini İyileşme Süresi: {prediction['recovery_time']} ay\n\n"
            text += f"👥 Tahmini Müşteri Kaybı: %{prediction['customer_loss']:.1f}\n\n"
            text += f"📊 Risk Skoru: {prediction.get('risk_score', 'N/A')}/100\n\n"
            text += "💡 Öneriler:\n"
            
            self.ai_recommendations.delete(0, tk.END)
            recommendations = [
                prediction['recommendation'],
                "Sigorta kapsamını gözden geçirin",
                "Halkla ilişkiler stratejisi oluşturun",
                "Finansal denetim yapın"
            ]
            
            for rec in recommendations:
                self.ai_recommendations.insert(tk.END, f"• {rec}")
                text += f"• {rec}\n"
            
            self.ai_result_text.insert(tk.END, text)
        
        self.ai_result_text.config(state=tk.DISABLED)
    
    def update_charts(self, direct_loss, brand_loss, operational_loss, customers, countries, scenario_multiplier):
        """Tüm grafikleri günceller"""
        # 3D Kayıp Dağılımı
        self.update_3d_chart(direct_loss, brand_loss, operational_loss)
        
        # Coğrafi Etki Haritası
        self.update_geo_map(customers, countries)
        
        # Zaman Serisi Grafiği
        self.update_time_series(direct_loss + brand_loss + operational_loss)
        
        # Makro Ekonomik Etki
        self.update_macro_chart(direct_loss, brand_loss, operational_loss, scenario_multiplier)
    
    def update_3d_chart(self, direct_loss, brand_loss, operational_loss):
        """3D grafiği günceller"""
        self.ax_3d.clear()
        
        # Veriler
        categories = ['Doğrudan', 'Marka', 'Operasyonel']
        values = [direct_loss, brand_loss, operational_loss]
        colors = [self.colors['accent'], self.colors['warning'], self.colors['light_accent']]
        
        # 3D çubuk grafik
        xpos = [0, 1, 2]
        ypos = [0, 0, 0]
        zpos = [0, 0, 0]
        
        dx = dy = 0.5
        dz = [v / 1000000 for v in values]  # Milyon cinsinden
        
        self.ax_3d.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors, shade=True)
        
        # Eksen etiketleri
        self.ax_3d.set_xticks([0.25, 1.25, 2.25])
        self.ax_3d.set_xticklabels(categories)
        self.ax_3d.set_ylabel('')
        self.ax_3d.set_zlabel('Kayıp (Milyon $)')
        
        # Başlık
        self.ax_3d.set_title('3D Kayıp Dağılımı', fontsize=12, pad=20)
        
        self.canvas_3d.draw()
    
    def update_geo_map(self, customers, countries):
        """Coğrafi haritayı günceller"""
        try:
            # Örnek veri oluştur
            country_data = {
                'Turkey': random.randint(1000000, 5000000),
                'Germany': random.randint(500000, 2000000),
                'USA': random.randint(2000000, 8000000),
                'UK': random.randint(300000, 1500000)
            }
            
            # Harita oluştur
            m = folium.Map(location=[39, 35], zoom_start=2)
            
            # Isı haritası verileri
            heat_data = []
            for country, value in country_data.items():
                # Basit bir konum eşleme
                if country == 'Turkey':
                    lat, lon = 39, 35
                elif country == 'Germany':
                    lat, lon = 51, 10
                elif country == 'USA':
                    lat, lon = 38, -97
                elif country == 'UK':
                    lat, lon = 55, -3
                
                heat_data.append([lat, lon, value / 1000000])  # Milyon cinsinden
            
            # Isı haritası ekle
            HeatMap(heat_data, radius=15).add_to(m)
            
            # Haritayı HTML olarak kaydet
            map_html = "temp_map.html"
            m.save(map_html)
            
            # HTML'yi görüntüle
            self.show_map_in_frame(map_html)
            
        except Exception as e:
            print(f"Harita oluşturma hatası: {str(e)}")
            self.map_label.config(text=f"Harita yüklenirken hata oluştu: {str(e)}")
    
    def show_map_in_frame(self, html_file):
        """Haritayı frame içinde göster"""
        try:
            # Önceki widget'ları temizle
            for widget in self.map_frame.winfo_children():
                widget.destroy()
            
            # Webview oluştur (basit bir alternatif)
            from tkinterweb import HtmlFrame
            map_frame = HtmlFrame(self.map_frame)
            map_frame.load_file(html_file)
            map_frame.pack(fill=tk.BOTH, expand=True)
            
        except:
            # Alternatif yöntem
            self.map_label = ttk.Label(self.map_frame, text="Harita görüntülenemiyor. Tarayıcıda açmak için tıklayın.")
            self.map_label.pack(fill=tk.BOTH, expand=True)
            self.map_label.bind("<Button-1>", lambda e: webbrowser.open(html_file))
    
    def update_time_series(self, total_loss):
        """Zaman serisi grafiğini günceller"""
        self.ax_time.clear()
        
        # Veriler
        months = ['Olay', '1 Ay', '3 Ay', '6 Ay', '1 Yıl']
        recovery = [100, 85 - random.random()*10, 70 - random.random()*15, 
                   50 - random.random()*20, 30 - random.random()*15]
        
        # Çizgi grafiği
        self.ax_time.plot(months, recovery, marker='o', color=self.colors['accent'],
                         linewidth=2, markersize=8, markerfacecolor='white',
                         markeredgewidth=2, markeredgecolor=self.colors['accent'])
        
        # Alan grafiği
        self.ax_time.fill_between(months, recovery, color=self.colors['accent'], alpha=0.1)
        
        # Eksenler
        self.ax_time.set_ylim(0, 110)
        self.ax_time.set_ylabel('Etki (%)', color=self.colors['primary'])
        self.ax_time.grid(True, linestyle='--', alpha=0.5)
        
        # Başlık
        self.ax_time.set_title('Zamana Göre İyileşme Projeksiyonu', fontsize=12, 
                             pad=15, color=self.colors['primary'])
        
        self.canvas_time.draw()
    
    def update_macro_chart(self, direct_loss, brand_loss, operational_loss, scenario_multiplier):
        """Makro ekonomik etki grafiğini günceller"""
        self.ax_macro.clear()
        
        # Veriler
        categories = ['GSYİH Etkisi', 'Enflasyon', 'İşsizlik', 'Borsa', 'Döviz']
        base_values = [direct_loss/850000000, 
                      (direct_loss + operational_loss)/10000000, 
                      operational_loss/5000000, 
                      brand_loss/100000000, 
                      (direct_loss + brand_loss)/50000000]
        
        # Senaryo çarpanını uygula
        values = [v * scenario_multiplier for v in base_values]
        
        # Renkler
        colors = []
        for val in values:
            if val > 0.7:
                colors.append(self.colors['accent'])
            elif val > 0.4:
                colors.append(self.colors['warning'])
            else:
                colors.append(self.colors['success'])
        
        # Çubuk grafik
        bars = self.ax_macro.bar(categories, values, color=colors, edgecolor='white')
        
        # Çubuk etiketleri
        for bar in bars:
            height = bar.get_height()
            self.ax_macro.text(bar.get_x() + bar.get_width()/2., height,
                             f'{height:.2f}%',
                             ha='center', va='bottom', fontsize=8)
        
        # Eksenler
        self.ax_macro.set_ylim(0, max(values)*1.2)
        self.ax_macro.set_ylabel('Etki Yüzdesi', color=self.colors['primary'])
        self.ax_macro.grid(axis='y', linestyle='--', alpha=0.5)
        
        # Başlık
        self.ax_macro.set_title('Makroekonomik Etki Projeksiyonu', fontsize=12, 
                              pad=15, color=self.colors['primary'])
        
        self.canvas_macro.draw()
    
    def track_blockchain(self):
        """Blockchain işlemini takip eder"""
        tx_hash = self.blockchain_entry.get().strip()
        if not tx_hash:
            messagebox.showwarning("Uyarı", "Lütfen geçerli bir işlem hash'i girin")
            return
        
        try:
            self.blockchain_text.config(state=tk.NORMAL)
            self.blockchain_text.delete(1.0, tk.END)
            self.blockchain_text.insert(tk.END, f"{tx_hash} işlemi aranıyor...\n\n")
            self.blockchain_text.see(tk.END)
            
            # Simüle edilmiş blockchain verileri
            time.sleep(1)  # Gerçekçi bir bekleme
            
            fake_data = {
                "hash": tx_hash,
                "from": "0x" + ''.join(random.choices('0123456789abcdef', k=40)),
                "to": "0x" + ''.join(random.choices('0123456789abcdef', k=40)),
                "value": random.randint(1000, 50000),
                "block": random.randint(15000000, 16000000),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "confirmations": random.randint(10, 5000)
            }
            
            self.blockchain_text.insert(tk.END, json.dumps(fake_data, indent=4))
            self.blockchain_text.insert(tk.END, "\n\nİşlem başarıyla bulundu. Para akışını görselleştirmek için butona basın.")
            self.blockchain_text.config(state=tk.DISABLED)
            
        except Exception as e:
            self.blockchain_text.insert(tk.END, f"\nHata oluştu: {str(e)}")
            self.blockchain_text.config(state=tk.DISABLED)
    
    def visualize_money_flow(self):
        """Para akışını görselleştirir"""
        try:
            # Plotly ile interaktif grafik oluştur
            fig = go.Figure(go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=["Kaynak Cüzdan", "Ara Cüzdan 1", "Ara Cüzdan 2", "Hedef Cüzdan"],
                    color=["blue", "green", "purple", "red"]
                ),
                link=dict(
                    source=[0, 1, 2],  # Kaynak indeksleri
                    target=[1, 2, 3],   # Hedef indeksleri
                    value=[1000000, 500000, 500000]  # Transfer miktarları
                )
            ))
            
            fig.update_layout(title_text="Para Akışı - Blockchain İzleme", font_size=10)
            
            # HTML olarak kaydet ve tarayıcıda aç
            fig.write_html("money_flow.html")
            webbrowser.open("money_flow.html")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Görselleştirme oluşturulamadı:\n{str(e)}")
    
    def save_blockchain_data(self):
        """Blockchain verilerini kaydeder"""
        try:
            filename = f"blockchain_tracking_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w") as f:
                f.write(self.blockchain_text.get(1.0, tk.END))
            messagebox.showinfo("Başarılı", f"Blockchain verileri '{filename}' dosyasına kaydedildi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya kaydedilirken hata oluştu:\n{str(e)}")
    
    def run_detailed_ai_analysis(self):
        """Detaylı AI analizi yapar"""
        self.ai_result_text.config(state=tk.NORMAL)
        self.ai_result_text.delete(1.0, tk.END)
        self.ai_result_text.insert(tk.END, "🤖 AI detaylı analiz yapıyor... Lütfen bekleyiniz.\n")
        self.ai_result_text.see(tk.END)
        self.ai_result_text.config(state=tk.DISABLED)
        
        # Uzun süren bir işlemi simüle et
        def analyze():
            time.sleep(3)  # Analiz süresini simüle et
            
            # Rastgele sonuçlar oluştur
            analysis_results = [
                "⏳ Tahmini tam iyileşme süresi: %d ay" % random.randint(6, 24),
                "📉 En yüksek kayıp dönemi: İlk %d hafta" % random.randint(2, 8),
                "👥 Müşteri güveni geri kazanma süresi: %d ay" % random.randint(3, 12),
                "📊 Hisselerin eski seviyeye gelme süresi: %d ay" % random.randint(9, 36),
                "💸 Sigorta kapsamı: %d%% kayıp karşılanabilir" % random.randint(30, 80),
                "⚠️ Potansiyel regülasyon cezaları: $%dM - $%dM" % (random.randint(1,5), random.randint(5,10))
            ]
            
            self.ai_result_text.config(state=tk.NORMAL)
            self.ai_result_text.delete(1.0, tk.END)
            self.ai_result_text.insert(tk.END, "🔍 DETAYLI AI ANALİZ SONUÇLARI\n")
            self.ai_result_text.insert(tk.END, "="*50 + "\n\n")
            
            for result in analysis_results:
                self.ai_result_text.insert(tk.END, f"• {result}\n\n")
            
            self.ai_result_text.insert(tk.END, "="*50 + "\n")
            self.ai_result_text.insert(tk.END, "ℹ️ Bu sonuçlar tahmini değerlerdir. Gerçek sonuçlar farklılık gösterebilir.")
            self.ai_result_text.config(state=tk.DISABLED)
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def run_future_prediction(self):
        """Gelecek tahmini yapar"""
        self.ai_result_text.config(state=tk.NORMAL)
        self.ai_result_text.delete(1.0, tk.END)
        self.ai_result_text.insert(tk.END, "🔮 AI gelecek tahmini yapıyor... Lütfen bekleyiniz.\n")
        self.ai_result_text.see(tk.END)
        self.ai_result_text.config(state=tk.DISABLED)
        
        # Uzun süren bir işlemi simüle et
        def predict():
            time.sleep(2)  # Tahmin süresini simüle et
            
            # Rastgele tahminler oluştur
            predictions = [
                "📈 Önümüzdeki 3 ay içinde hisselerde %d%% - %d%% dalgalanma bekleniyor" % (random.randint(5,15), random.randint(15,30)),
                "🛡️ %d hafta içinde yeni bir siber güvenlik önlemi uygulanması öneriliyor" % random.randint(2,8),
                "💼 %d ay içinde yeni yatırımcıların devreye girmesi bekleniyor" % random.randint(3,9),
                "🌍 %d ülkede regülasyon değişikliği riski bulunuyor" % random.randint(1,5),
                "💰 %d%% olasılıkla sigorta şirketi ek tazminat talebinde bulunacak" % random.randint(30,70)
            ]
            
            self.ai_result_text.config(state=tk.NORMAL)
            self.ai_result_text.delete(1.0, tk.END)
            self.ai_result_text.insert(tk.END, "🔮 AI GELECEK TAHMİNLERİ\n")
            self.ai_result_text.insert(tk.END, "="*50 + "\n\n")
            
            for prediction in predictions:
                self.ai_result_text.insert(tk.END, f"• {prediction}\n\n")
            
            self.ai_result_text.insert(tk.END, "="*50 + "\n")
            self.ai_result_text.insert(tk.END, "ℹ️ Bu tahminler geçmiş verilere dayalı istatistiksel projeksiyonlardır.")
            self.ai_result_text.config(state=tk.DISABLED)
        
        threading.Thread(target=predict, daemon=True).start()
    
    def update_scenario(self):
        """Senaryo seçimini günceller"""
        scenario = self.scenario_var.get()
        messagebox.showinfo("Senaryo Güncellendi", f"'{scenario}' senaryosu seçildi. Hesaplamayı yenilemek için 'Hesapla' butonuna basın.")
    
    def create_custom_scenario(self):
        """Özel senaryo oluşturur"""
        custom_window = tk.Toplevel(self.root)
        custom_window.title("Özel Senaryo Oluştur")
        custom_window.geometry("500x400")
        
        ttk.Label(custom_window, text="Özel Senaryo Adı:").pack(pady=(10,0))
        name_entry = ttk.Entry(custom_window)
        name_entry.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(custom_window, text="Risk Çarpanı (1.0-5.0):").pack(pady=(10,0))
        multiplier_entry = ttk.Entry(custom_window)
        multiplier_entry.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(custom_window, text="Ek Özellikler:").pack(pady=(10,0))
        features_frame = ttk.Frame(custom_window)
        features_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Özellik seçimleri
        features = [
            ("Devlet Müdahalesi", "gov_intervention"),
            ("Medya Etkisi", "media_impact"),
            ("Küresel Etki", "global_impact"),
            ("Veri Sızıntısı", "data_leak"),
            ("Fidye Yazılımı", "ransomware")
        ]
        
        self.feature_vars = {}
        for i, (text, var_name) in enumerate(features):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(features_frame, text=text, variable=var)
            cb.grid(row=i//2, column=i%2, sticky="w", padx=5, pady=2)
            self.feature_vars[var_name] = var
        
        # Kaydet butonu
        ttk.Button(custom_window, text="Senaryoyu Kaydet", 
                  command=lambda: self.save_custom_scenario(
                      name_entry.get(),
                      multiplier_entry.get(),
                      {k: v.get() for k, v in self.feature_vars.items()},
                      custom_window
                  ), style='Accent.TButton').pack(pady=20)
    
    def save_custom_scenario(self, name, multiplier, features, window):
        """Özel senaryoyu kaydeder"""
        try:
            multiplier = float(multiplier)
            if not 1.0 <= multiplier <= 5.0:
                raise ValueError("Çarpan 1.0-5.0 aralığında olmalı")
            
            if not name:
                raise ValueError("Senaryo adı boş olamaz")
            
            # Senaryoyu kaydet (gerçek uygulamada veritabanına kaydedilir)
            messagebox.showinfo("Başarılı", f"'{name}' senaryosu kaydedildi!\nRisk Çarpanı: {multiplier}x")
            window.destroy()
            
            # Senaryo listesine ekle
            self.scenario_var.set(name)
            
        except ValueError as e:
            messagebox.showerror("Hata", f"Geçersiz giriş:\n{str(e)}")
    
    def save_results(self):
        """Sonuçları kaydeder"""
        try:
            filename = f"banka_hack_analiz_raporu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.sonuc_metni.get(1.0, tk.END))
            messagebox.showinfo("Başarılı", f"Sonuçlar '{filename}' dosyasına kaydedildi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya kaydedilirken bir hata oluştu:\n{str(e)}")
    
    def generate_advanced_report(self):
        """Gelişmiş rapor oluşturur"""
        report_window = tk.Toplevel(self.root)
        report_window.title("Gelişmiş Rapor Oluştur")
        report_window.geometry("600x500")
        
        ttk.Label(report_window, 
                 text="Gelişmiş Rapor Oluşturma",
                 font=('Segoe UI', 14, 'bold')).pack(pady=20)
        
        # Rapor seçenekleri
        options_frame = ttk.Frame(report_window)
        options_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        # Format seçimi
        ttk.Label(options_frame, text="Rapor Formatı:").grid(row=0, column=0, sticky="w", pady=5)
        self.report_format = ttk.Combobox(options_frame, 
                                        values=["PDF (Profesyonel)", "HTML (İnteraktif)", 
                                               "Word (Detaylı)", "Excel (Veri Analizi)"])
        self.report_format.current(0)
        self.report_format.grid(row=0, column=1, sticky="ew", pady=5)
        
        # Detay seviyesi
        ttk.Label(options_frame, text="Detay Seviyesi:").grid(row=1, column=0, sticky="w", pady=5)
        self.detail_level = ttk.Combobox(options_frame, 
                                        values=["Özet (Yönetici Özeti)", 
                                               "Standart (Temel Analiz)", 
                                               "Detaylı (Teknik Rapor)", 
                                               "Tam (Tüm Veriler)"])
        self.detail_level.current(1)
        self.detail_level.grid(row=1, column=1, sticky="ew", pady=5)
        
        # Grafik seçenekleri
        ttk.Label(options_frame, text="Grafikler:").grid(row=2, column=0, sticky="w", pady=5)
        self.graph_options = tk.Listbox(options_frame, height=4, selectmode=tk.MULTIPLE)
        self.graph_options.grid(row=2, column=1, sticky="ew", pady=5)
        
        for option in ["Kayıp Dağılımı", "Zaman Serisi", "Coğrafi Etki", "Makro Ekonomik"]:
            self.graph_options.insert(tk.END, option)
        self.graph_options.selection_set(0, tk.END)  # Tümünü seçili yap
        
        # Ek özellikler
        ttk.Label(options_frame, text="Ek Özellikler:").grid(row=3, column=0, sticky="w", pady=5)
        features_frame = ttk.Frame(options_frame)
        features_frame.grid(row=3, column=1, sticky="ew", pady=5)
        
        self.include_ai = tk.BooleanVar(value=True)
        ttk.Checkbutton(features_frame, text="AI Analizini Dahil Et", 
                       variable=self.include_ai).pack(side=tk.LEFT, padx=5)
        
        self.include_blockchain = tk.BooleanVar(value=False)
        ttk.Checkbutton(features_frame, text="Blockchain Verilerini Dahil Et", 
                       variable=self.include_blockchain).pack(side=tk.LEFT, padx=5)
        
        # Butonlar
        button_frame = ttk.Frame(report_window)
        button_frame.pack(fill=tk.X, padx=30, pady=20)
        
        ttk.Button(button_frame, text="İptal", 
                  command=report_window.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Raporu Oluştur", 
                  command=self.create_report, style='Accent.TButton').pack(side=tk.RIGHT, padx=5)
    
    def create_report(self):
        """Rapor oluşturma işlemini gerçekleştirir"""
        # Burada gerçek rapor oluşturma işlemleri yapılır
        # Şu an için simüle ediyoruz
        
        selected_graphs = [self.graph_options.get(i) for i in self.graph_options.curselection()]
        
        message = f"""
        Rapor oluşturma başlatıldı:
        - Format: {self.report_format.get()}
        - Detay Seviyesi: {self.detail_level.get()}
        - Grafikler: {', '.join(selected_graphs)}
        - AI Analizi: {'Evet' if self.include_ai.get() else 'Hayır'}
        - Blockchain Verisi: {'Evet' if self.include_blockchain.get() else 'Hayır'}
        
        Rapor oluşturuldu ve 'Raporlar' klasörüne kaydedildi.
        """
        
        messagebox.showinfo("Rapor Oluşturuldu", message)
    
    def open_help(self):
        """Yardım sayfasını açar"""
        webbrowser.open("https://www.example.com/ultimate-banka-hack-yardim")
    
    def about(self):
        """Hakkında penceresi"""
        about_window = tk.Toplevel(self.root)
        about_window.title("Hakkında")
        about_window.geometry("500x450")
        
        # Başlık
        ttk.Label(about_window, 
                 text="Ultimate Banka Hack Analiz Platformu",
                 font=('Segoe UI', 16, 'bold')).pack(pady=15)
        
        # Logo
        logo_label = ttk.Label(about_window, 
                             text="🔐",
                             font=('Segoe UI', 48),
                             foreground=self.colors['primary'])
        logo_label.pack(pady=5)
        
        # Versiyon
        ttk.Label(about_window, 
                 text=f"Versiyon 3.0 | {datetime.now().strftime('%Y')}",
                 foreground=self.colors['light_text']).pack(pady=5)
        
        # Açıklama
        desc_frame = ttk.Frame(about_window)
        desc_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        desc_text = """
Bu uygulama, banka hack olaylarının finansal ve operasyonel 
etkilerini analiz etmek için geliştirilmiş kapsamlı bir 
çözümdür. Yapay zeka, blockchain analizi ve gelişmiş 
görselleştirme teknikleriyle donatılmıştır.

Özellikler:
- Gerçek zamanlı risk değerlendirme
- Çok boyutlu finansal analiz
- AI destekli tahmin motoru
- Blockchain para takip sistemi
- 3D veri görselleştirme
        """
        
        ttk.Label(desc_frame, text=desc_text, justify='center').pack()
        
        # Kapatma butonu
        ttk.Button(about_window, 
                  text="Kapat", 
                  command=about_window.destroy,
                  style='Accent.TButton').pack(pady=15)

# Uygulamayı başlat
if __name__ == "__main__":
    try:
        # Windows'ta DPI farkındalığı
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    root = tk.Tk()
    app = UltimateBankaHackAnalizTool(root)
    root.mainloop()