import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import font as tkfont
import webbrowser
from datetime import datetime

class ModernBankaHackAnalizTool:
    def __init__(self, root):
        self.root = root
        self.root.title("🔒 Banka Hack Ekonomik Etki Analiz Aracı v2.0")
        self.root.geometry("1280x900")
        self.root.configure(bg='#f8f9fa')
        
        # Modern renk şeması
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#34495e',
            'accent': '#e74c3c',
            'light_accent': '#3498db',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'background': '#f8f9fa',
            'text': '#2c3e50',
            'light_text': '#7f8c8d'
        }
        
        # Stil ayarları
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
        self.style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), 
                           foreground=self.colors['primary'])
        self.style.configure('Accent.TButton', foreground='white', 
                           background=self.colors['accent'])
        self.style.configure('Secondary.TButton', foreground='white', 
                           background=self.colors['light_accent'])
        self.style.configure('Link.TButton', foreground=self.colors['light_accent'], 
                           borderwidth=0, background=self.colors['background'])
        
        self.style.map('TButton', 
                      background=[('active', self.colors['secondary'])])
        self.style.map('Accent.TButton', 
                      background=[('active', '#c0392b')])
        self.style.map('Secondary.TButton', 
                      background=[('active', '#2980b9')])
        
        # Başlık
        self.create_header()
        
        # Ana içerik
        self.create_main_content()
        
        # Footer
        self.create_footer()
        
        # Başlangıçta örnek veri yükle
        self.load_sample_data()
        
    def create_header(self):
        header_frame = ttk.Frame(self.root, style='TFrame')
        header_frame.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        # Logo ve başlık
        logo_frame = ttk.Frame(header_frame, style='TFrame')
        logo_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.logo_label = ttk.Label(logo_frame, 
                                  text="🔐", 
                                  font=('Segoe UI', 24),
                                  background=self.colors['background'])
        self.logo_label.pack(side=tk.LEFT, padx=(0, 10))
        
        title_frame = ttk.Frame(logo_frame, style='TFrame')
        title_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        title_label = ttk.Label(title_frame, 
                              text="BANKA HACK ANALİZ PLATFORMU", 
                              style='Header.TLabel')
        title_label.pack(anchor='w')
        
        subtitle_label = ttk.Label(title_frame, 
                                 text="Siber Güvenlik & Finansal Etki Değerlendirme Aracı",
                                 foreground=self.colors['light_text'])
        subtitle_label.pack(anchor='w')
        
        # Sağ taraf - versiyon ve tarih
        info_frame = ttk.Frame(header_frame, style='TFrame')
        info_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        version_label = ttk.Label(info_frame, 
                                text=f"v2.0 | {datetime.now().strftime('%d.%m.%Y')}",
                                foreground=self.colors['light_text'])
        version_label.pack(anchor='e')
        
        status_label = ttk.Label(info_frame, 
                               text="✓ Çevrimiçi | Veri Güvenliği Aktif",
                               foreground=self.colors['success'])
        status_label.pack(anchor='e', pady=(5,0))
        
    def create_main_content(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0,15))
        
        # Sol panel - Giriş alanları
        self.create_input_panel(main_frame)
        
        # Orta panel - Sonuçlar
        self.create_results_panel(main_frame)
        
        # Sağ panel - Grafikler
        self.create_graph_panel(main_frame)
        
        # Grid ayarları
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=2)
        main_frame.rowconfigure(0, weight=1)
    
    def create_input_panel(self, parent):
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
            ("Saatlik İşlem Hacmi ($):", "saatlik_islem", "1000000")
        ]
        
        for i, (label_text, attr_name, default_value) in enumerate(entries):
            frame = ttk.Frame(input_frame, style='TFrame')
            frame.grid(row=i, column=0, sticky="ew", pady=4)
            
            label = ttk.Label(frame, text=label_text, width=25, anchor='w')
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
                  command=self.hesapla, style='Accent.TButton').pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Risk göstergesi
        risk_frame = ttk.LabelFrame(input_frame, text="  RİSK DEĞERLENDİRME  ", padding=(10, 5))
        risk_frame.grid(row=len(entries)+2, column=0, sticky="ew", pady=(20,5))
        
        self.risk_meter = ttk.Label(risk_frame, text="Hesaplama yapılmadı", 
                                  background='white', anchor='center',
                                  font=('Segoe UI', 9), padding=(5,5))
        self.risk_meter.pack(fill=tk.X)
        
        # Ek bilgi
        info_label = ttk.Label(input_frame, 
                              text="Tüm alanları doldurduktan sonra 'Hesapla' butonuna basın.",
                              foreground=self.colors['light_text'], font=('Segoe UI', 9))
        info_label.grid(row=len(entries)+3, column=0, sticky="ew", pady=(10,0))
    
    def create_results_panel(self, parent):
        results_frame = ttk.LabelFrame(parent, text="  ANALİZ SONUÇLARI  ", padding=(15, 12))
        results_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        
        # Sonuç metni için scrollbar
        scroll_frame = ttk.Frame(results_frame)
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
        button_frame = ttk.Frame(results_frame)
        button_frame.pack(fill=tk.X, pady=(10,0))
        
        ttk.Button(button_frame, text="Sonuçları Kaydet", 
                  command=self.save_results, style='Secondary.TButton').pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(button_frame, text="Rapor Oluştur", 
                  command=self.generate_report, style='Secondary.TButton').pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Hızlı istatistikler
        stats_frame = ttk.LabelFrame(results_frame, text="  HIZLI İSTATİSTİKLER  ", padding=(10, 8))
        stats_frame.pack(fill=tk.X, pady=(15,0))
        
        self.stats_labels = []
        for i in range(3):
            lbl = ttk.Label(stats_frame, text="---", 
                          font=('Segoe UI', 9), 
                          background='white', 
                          padding=(5,5),
                          anchor='center')
            lbl.pack(fill=tk.X, pady=2)
            self.stats_labels.append(lbl)
    
    def create_graph_panel(self, parent):
        graph_frame = ttk.LabelFrame(parent, text="  GÖRSEL ANALİZ  ", padding=(15, 12))
        graph_frame.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")
        
        # Notebook (sekme) yapısı
        self.notebook = ttk.Notebook(graph_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Grafik 1 sekmesi
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="Kayıp Dağılımı")
        
        self.fig, self.ax = plt.subplots(figsize=(8, 5), facecolor=self.colors['background'])
        self.fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        self.canvas = FigureCanvasTkAgg(self.fig, master=tab1)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Grafik 2 sekmesi
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="Detaylı Analiz")
        
        self.fig2, self.ax2 = plt.subplots(figsize=(8, 4), facecolor=self.colors['background'])
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=tab2)
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Grafik 3 sekmesi (Zaman Serisi)
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text="Zaman Etkisi")
        
        self.fig3, self.ax3 = plt.subplots(figsize=(8, 3), facecolor=self.colors['background'])
        self.canvas3 = FigureCanvasTkAgg(self.fig3, master=tab3)
        self.canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Grafik ayarları
        plt.style.use('seaborn-v0_8')  # Düzeltildi
    
    def create_footer(self):
        footer_frame = ttk.Frame(self.root, style='TFrame')
        footer_frame.pack(fill=tk.X, padx=20, pady=(0,15))
        
        # Sosyal medya butonları
        social_frame = ttk.Frame(footer_frame, style='TFrame')
        social_frame.pack(side=tk.LEFT)
        
        social_links = [
            ("🌐", "https://www.example.com"),
            ("📘", "https://www.facebook.com"),
            ("🐦", "https://www.twitter.com"),
            ("📷", "https://www.instagram.com"),
            ("💼", "https://www.linkedin.com")
        ]
        
        for icon, url in social_links:
            btn = ttk.Button(social_frame, text=icon, style='Link.TButton',
                           command=lambda u=url: webbrowser.open(u))
            btn.pack(side=tk.LEFT, padx=3)
        
        # Copyright ve diğer bilgiler
        info_frame = ttk.Frame(footer_frame, style='TFrame')
        info_frame.pack(side=tk.RIGHT)
        
        ttk.Label(info_frame, 
                 text="© 2025 Siber Güvenlik ve Finansal Analiz Ekibi | Tüm hakları saklıdır",
                 foreground=self.colors['light_text']).pack(side=tk.RIGHT)
        
        # Yardım butonları
        help_frame = ttk.Frame(footer_frame, style='TFrame')
        help_frame.pack(side=tk.RIGHT, padx=20)
        
        ttk.Button(help_frame, text="Yardım", 
                  command=self.open_help, style='Link.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(help_frame, text="Hakkında", 
                  command=self.about, style='Link.TButton').pack(side=tk.LEFT, padx=5)
    
    def load_sample_data(self):
        """Örnek veri yükleme fonksiyonu"""
        entries = [
            ("banka_adi", "Örnek Banka A.Ş."),
            ("calinan_miktar", "50000000"),
            ("onarim_maliyeti", "2000000"),
            ("yasal_cezalar", "5000000"),
            ("hisse_kaybi", "15"),
            ("piyasa_degeri", "1000000000"),
            ("kesinti_suresi", "24"),
            ("saatlik_islem", "1000000")
        ]
        
        for attr_name, value in entries:
            entry = getattr(self, attr_name)
            entry.delete(0, tk.END)
            entry.insert(0, value)
        
        self.risk_meter.config(text="Örnek veriler yüklendi. Hesaplamak için 'Hesapla' butonuna basın.",
                             background=self.colors['warning'], foreground='white')
    
    def hesapla(self):
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
            
            # Hesaplamalar
            toplam_dogrudan_kayip = calinan + onarim + ceza
            marka_degeri_kaybi = hisse_kayip * piyasa_deger
            operasyonel_kayip = kesinti * saatlik_islem
            toplam_kayip = toplam_dogrudan_kayip + marka_degeri_kaybi + operasyonel_kayip
            
            # GSYİH karşılaştırması (Türkiye için yaklaşık 850 milyar $)
            gsyih_oran = (toplam_kayip/850000000000)*100
            
            # Risk seviyesini belirle
            risk_seviyesi = "DÜŞÜK"
            risk_rengi = self.colors['success']
            if toplam_kayip > 100000000:
                risk_seviyesi = "YÜKSEK"
                risk_rengi = self.colors['accent']
            elif toplam_kayip > 50000000:
                risk_seviyesi = "ORTA"
                risk_rengi = self.colors['warning']
            
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
            sonuc_text += f"  • Risk Seviyesi: {risk_seviyesi}\n"
            sonuc_text += "="*50 + "\n"
            sonuc_text += "⚠️ Uyarı: Bu sonuçlar tahmini değerlerdir. Detaylı analiz için uzman görüşü alınız."
            
            self.sonuc_metni.config(state=tk.NORMAL)
            self.sonuc_metni.delete(1.0, tk.END)
            self.sonuc_metni.insert(tk.END, sonuc_text)
            self.sonuc_metni.config(state=tk.DISABLED)
            
            # Hızlı istatistikleri güncelle
            self.stats_labels[0].config(text=f"Toplam Kayıp: ${toplam_kayip/1000000:,.1f} Milyon")
            self.stats_labels[1].config(text=f"Risk Seviyesi: {risk_seviyesi}")
            self.stats_labels[2].config(text=f"GSYİH Etkisi: %{gsyih_oran:.4f}")
            
            # Risk göstergesini güncelle
            self.risk_meter.config(text=f"RİSK SEVİYESİ: {risk_seviyesi} | Toplam Kayıp: ${toplam_kayip/1000000:,.1f}M",
                                 background=risk_rengi, foreground='white',
                                 font=('Segoe UI', 10, 'bold'))
            
            # Grafik oluştur
            self.create_charts(toplam_dogrudan_kayip, marka_degeri_kaybi, operasyonel_kayip)
            
        except ValueError:
            messagebox.showerror("Hata", "Lütfen tüm alanları doğru şekilde doldurun!")
            self.risk_meter.config(text="Geçersiz veri girişi! Lütfen kontrol edin.",
                                 background=self.colors['accent'], foreground='white')
    
    def create_charts(self, dogrudan, marka, operasyonel):
        """Grafikleri oluşturur"""
        # Ana grafik - Pasta grafiği
        self.ax.clear()
        
        labels = ['Doğrudan Kayıplar', 'Marka Değeri Kaybı', 'Operasyonel Kayıp']
        sizes = [dogrudan, marka, operasyonel]
        colors = [self.colors['accent'], self.colors['warning'], self.colors['light_accent']]
        explode = (0.05, 0, 0)
        
        wedges, texts, autotexts = self.ax.pie(
            sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90,
            textprops={'fontsize': 9}, wedgeprops={'edgecolor': 'white', 'linewidth': 1}
        )
        
        # Yüzde değerlerini daha okunaklı yap
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        self.ax.set_title('Kayıp Dağılımı', fontsize=12, pad=20, color=self.colors['primary'])
        
        # İkincil grafik - Çubuk grafik
        self.ax2.clear()
        
        categories = ['Çalınan Para', 'Onarım', 'Cezalar', 'Hisse Kaybı', 'Operasyonel']
        values = [dogrudan/3, dogrudan/3, dogrudan/3, marka, operasyonel]  # Düzeltildi: dogruan -> dogrudan
        
        bars = self.ax2.bar(categories, values, color=[
            self.colors['accent'], '#e67e22', '#d35400', 
            self.colors['warning'], self.colors['light_accent']
        ], edgecolor='white')
        
        self.ax2.set_title('Kayıp Kategorileri ($)', fontsize=12, pad=15, color=self.colors['primary'])
        self.ax2.tick_params(axis='x', rotation=45, labelsize=8)
        self.ax2.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Çubukların üzerine değerleri yaz
        for bar in bars:
            height = bar.get_height()
            self.ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'${height/1000000:,.1f}M',
                        ha='center', va='bottom', fontsize=8, color=self.colors['primary'])
        
        # Üçüncü grafik - Zaman serisi simülasyonu
        self.ax3.clear()
        
        months = ['Olay', '1 Ay', '3 Ay', '6 Ay', '1 Yıl']
        recovery = [100, 85, 70, 50, 30]  # İyileşme yüzdesi
        
        self.ax3.plot(months, recovery, marker='o', color=self.colors['accent'],
                     linewidth=2, markersize=8, markerfacecolor='white',
                     markeredgewidth=2, markeredgecolor=self.colors['accent'])
        
        self.ax3.fill_between(months, recovery, color=self.colors['accent'], alpha=0.1)
        self.ax3.set_title('Zamana Göre İyileşme Projeksiyonu', fontsize=12, 
                         pad=15, color=self.colors['primary'])
        self.ax3.set_ylabel('Etki (%)', color=self.colors['primary'])
        self.ax3.grid(True, linestyle='--', alpha=0.5)
        
        # Grafikleri çiz
        self.canvas.draw()
        self.canvas2.draw()
        self.canvas3.draw()
    
    def save_results(self):
        """Sonuçları dosyaya kaydeder"""
        try:
            filename = f"banka_hack_analiz_raporu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.sonuc_metni.get(1.0, tk.END))
            messagebox.showinfo("Başarılı", f"Sonuçlar '{filename}' dosyasına kaydedildi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya kaydedilirken bir hata oluştu:\n{str(e)}")
    
    def generate_report(self):
        """Rapor oluşturma fonksiyonu"""
        # Daha gelişmiş bir rapor penceresi
        report_window = tk.Toplevel(self.root)
        report_window.title("Rapor Oluştur")
        report_window.geometry("600x400")
        report_window.resizable(False, False)
        
        ttk.Label(report_window, 
                 text="Rapor Oluşturma Seçenekleri",
                 font=('Segoe UI', 12, 'bold')).pack(pady=10)
        
        # Rapor seçenekleri
        options_frame = ttk.Frame(report_window)
        options_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(options_frame, text="Rapor Formatı:").grid(row=0, column=0, sticky="w", pady=5)
        report_format = ttk.Combobox(options_frame, values=["PDF", "HTML", "Word", "Excel"])
        report_format.set("PDF")
        report_format.grid(row=0, column=1, sticky="ew", pady=5)
        
        ttk.Label(options_frame, text="Rapor Detay Seviyesi:").grid(row=1, column=0, sticky="w", pady=5)
        detail_level = ttk.Combobox(options_frame, values=["Özet", "Standart", "Detaylı"])
        detail_level.set("Standart")
        detail_level.grid(row=1, column=1, sticky="ew", pady=5)
        
        ttk.Label(options_frame, text="E-posta Gönder:").grid(row=2, column=0, sticky="w", pady=5)
        email_entry = ttk.Entry(options_frame)
        email_entry.grid(row=2, column=1, sticky="ew", pady=5)
        
        # Butonlar
        button_frame = ttk.Frame(report_window)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(button_frame, text="İptal", 
                  command=report_window.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Oluştur", 
                  command=lambda: self.create_actual_report(report_window, report_format.get(), detail_level.get(), email_entry.get()),
                  style='Accent.TButton').pack(side=tk.RIGHT, padx=5)
    
    def create_actual_report(self, window, format, detail, email):
        """Rapor oluşturma simülasyonu"""
        window.destroy()
        messagebox.showinfo("Başarılı", 
                          f"{detail} seviyesinde {format} raporu oluşturuldu!" + 
                          (f"\nRapor {email} adresine gönderildi." if email else ""))
    
    def open_help(self):
        """Yardım sayfasını açar"""
        webbrowser.open("https://www.example.com/banka-hack-analiz-yardim")
    
    def about(self):
        """Hakkında penceresi"""
        about_window = tk.Toplevel(self.root)
        about_window.title("Hakkında")
        about_window.geometry("500x400")
        about_window.resizable(False, False)
        
        # Başlık
        ttk.Label(about_window, 
                 text="Finanshield Analyzer",
                 font=('Segoe UI', 14, 'bold')).pack(pady=15)
        
        # Logo
        logo_label = ttk.Label(about_window, 
                             text="🔐",
                             font=('Segoe UI', 48),
                             foreground=self.colors['primary'])
        logo_label.pack(pady=5)
        
        # Açıklama
        desc_frame = ttk.Frame(about_window)
        desc_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        ttk.Label(desc_frame, 
                 text="Bu araç, banka hack olaylarının ekonomik etkisini analiz etmek için geliştirilmiştir.",
                 wraplength=400, justify='center').pack(pady=5)
        
        ttk.Label(desc_frame, 
                 text="Özellikler:",
                 font=('Segoe UI', 10, 'bold')).pack(pady=(15,5), anchor='w')
        
        features = [
            "✓ Finansal kayıp hesaplama",
            "✓ Marka değeri etki analizi",
            "✓ Operasyonel kesinti maliyeti",
            "✓ Makro ekonomik etki değerlendirmesi",
            "✓ Görsel analiz araçları"
        ]
        
        for feature in features:
            ttk.Label(desc_frame, 
                     text=feature,
                     foreground=self.colors['primary']).pack(anchor='w', padx=20)
        
        # Kapatma butonu
        ttk.Button(about_window, 
                  text="Kapat", 
                  command=about_window.destroy,
                  style='Accent.TButton').pack(pady=15)

# Uygulamayı başlat
if __name__ == "__main__":
    root = tk.Tk()
    
    # Windows'ta daha iyi görünüm için
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    app = ModernBankaHackAnalizTool(root)
    root.mainloop()