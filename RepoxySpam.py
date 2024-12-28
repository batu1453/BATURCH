import time
import requests
import tkinter as tk
from tkinter import messagebox
import webbrowser

# Renkler
PRIMARY_COLOR = '#00FF00'  # Yeşil (hacker tarzı)
SECONDARY_COLOR = '#333333'  # Siyah
BACKGROUND_COLOR = '#000000'  # Siyah arka plan
TEXT_COLOR = '#00FF00'  # Yeşil metin
BUTTON_COLOR = '#444444'  # Butonlar için koyu gri

def ngl():
    # Pencereyi oluştur
    root = tk.Tk()
    root.title("NGL Mesaj Gönderici")

    # Ekranın genişliği ve yüksekliğini al
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Pencereyi ekranda ortalamak için başlangıç konumu hesapla
    window_width = 600
    window_height = 400

    # Pencerenin konumunu biraz aşağı kaydır
    position_top = int(screen_height / 2 - window_height / 2) + 100  # 100px daha aşağı kaydırdım
    position_right = int(screen_width / 2 - window_width / 2)

    # Pencereyi belirtilen boyutlarla ve ortalanmış olarak ayarla
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
    
    # Pencere arka planını hacker tarzına uygun şekilde siyah yap
    root.config(bg=BACKGROUND_COLOR)

    # Başlık etiketini oluştur
    title_label = tk.Label(root, text="NGL Mesaj Gönderici", font=("Courier", 14, "bold"), fg=PRIMARY_COLOR, bg=BACKGROUND_COLOR)
    title_label.pack(pady=8)

    # Kullanıcı adı ve mesaj girişi
    username_label = tk.Label(root, text="Kullanıcı Adı:", font=("Courier", 10), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
    username_label.pack(pady=3)

    ngl_username_entry = tk.Entry(root, font=("Courier", 10), bd=2, highlightthickness=0, relief="solid", insertbackground=PRIMARY_COLOR)
    ngl_username_entry.pack(pady=5, ipadx=8, ipady=5, fill=tk.X)

    message_label = tk.Label(root, text="Mesaj:", font=("Courier", 10), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
    message_label.pack(pady=3)

    # Çok satırlı mesaj girişi
    message_text = tk.Text(root, height=4, font=("Courier", 10), bd=2, relief="solid", highlightthickness=0)
    message_text.pack(pady=5, fill=tk.X)

    # Durum etiketi
    status_label = tk.Label(root, text="Durum: Bekleniyor", font=("Courier", 10), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
    status_label.pack(pady=8)

    # Mesaj gönderme işlemi
    def send_messages():
        ngl_username = ngl_username_entry.get()
        message = message_text.get("1.0", tk.END).strip()  # Çok satırlı mesajdan veri al

        if not ngl_username or not message:
            messagebox.showerror("Hata", "Kullanıcı adı ve mesaj girmeniz gerekmektedir!")
            return
        
        gönderilen_mesaj_sayisi = 0
        while gönderilen_mesaj_sayisi < 20:  # 20 mesaj gönderildiğinde işlem duracak
            headers = {
                'Host': 'ngl.link',
                'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
                'accept': '*/*',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'x-requested-with': 'XMLHttpRequest',
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
                'sec-ch-ua-platform': '"Windows"',
                'origin': 'https://ngl.link',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': f'https://ngl.link/{ngl_username}',
                'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            }

            data = {
                'username': f'{ngl_username}',
                'question': f'{message}',
                'deviceId': '0',
                'gameSlug': '',
                'referrer': '',
            }

            try:
                response = requests.post('https://ngl.link/api/submit', headers=headers, data=data)
                if response.status_code == 200:
                    gönderilen_mesaj_sayisi += 1
                    status_label.config(text=f"Durum: {gönderilen_mesaj_sayisi} mesaj gönderildi", fg=PRIMARY_COLOR)
                elif response.status_code == 429:  # 429 hatası için bekleme süresi ekleyelim
                    status_label.config(text="Durum: Çok fazla istek, lütfen bekleyin...", fg=PRIMARY_COLOR)
                    time.sleep(10)  # 10 saniye bekleyelim
                else:
                    status_label.config(text=f"Durum: Hata, durum kodu {response.status_code}", fg=PRIMARY_COLOR)
                    break  # Gönderilemeyen istek sonrası işlemi sonlandır

            except requests.exceptions.RequestException as e:
                status_label.config(text=f"Durum: Hata oluştu", fg=PRIMARY_COLOR)
                break  # Hata oluşursa işlemi sonlandır

        if gönderilen_mesaj_sayisi == 20:
            messagebox.showinfo("Bilgi", "20 mesaj gönderildi, işlem durdu.")
            status_label.config(text="Durum: 20 mesaj gönderildi", fg=PRIMARY_COLOR)

            # Mesaj gönderildiğinde bir popup aç
            popup_message = tk.Toplevel()
            popup_message.title("Mesaj Gönderildi")
            popup_message.geometry("220x130")

            popup_label = tk.Label(popup_message, text="Mesajlar başarıyla gönderildi!", font=("Courier", 10), fg=PRIMARY_COLOR)
            popup_label.pack(pady=15)

            close_button = tk.Button(popup_message, text="Tamam", command=popup_message.destroy, bg=PRIMARY_COLOR, fg='black', relief="solid")
            close_button.pack()

    # Mesaj Gönder butonunu ekle
    send_button = tk.Button(root, text="Mesaj Gönder", font=("Courier", 12), bg=PRIMARY_COLOR, fg='black', relief="solid", command=send_messages)
    send_button.pack(pady=10, ipadx=18, ipady=8, fill=tk.X)

    # Tasarımcı Repo ve Pro versiyon butonlarını ekle
    def open_repo_site():
        webbrowser.open("https://baturch.vercel.app")

    def open_pro_version():
        webbrowser.open("https://shop.repoxy.xyz/contact.html")

    repo_button = tk.Button(root, text="TASARIMCI REPOXY MOBILE", font=("Courier", 12), bg=PRIMARY_COLOR, fg='black', relief="solid", command=open_repo_site)
    repo_button.pack(pady=10, ipadx=18, ipady=8, fill=tk.X)

    pro_version_button = tk.Button(root, text="PRO VERSİYON AL", font=("Courier", 12), bg=PRIMARY_COLOR, fg='black', relief="solid", command=open_pro_version)
    pro_version_button.pack(pady=10, ipadx=18, ipady=8, fill=tk.X)

    # Pencereyi çalıştır
    root.mainloop()

# Programı başlat
ngl()
