import http.client
import json
from tkinter import *
from datetime import datetime
import re
import sqlite3
from dotenv import load_dotenv
import os


Tarih = datetime.now().strftime("%Y/%m/%d %H:%M")


def veriTabanı_baslangic(Tarih, Ad, Kod, Deger):
    """Uygulama açılışında döviz verilerini kaydeder ve tarih listesini doldurur."""
    db = sqlite3.connect("../Doviz.db")
    yetki = db.cursor()

    yetki.execute("""
        CREATE TABLE IF NOT EXISTS Doviz(
            Tarih TEXT,
            Isim TEXT,
            Kod TEXT,
            BirTLKarsiligi REAL
        )
    """)

    # Aynı tarih+kod kombinasyonu zaten varsa tekrar ekleme
    yetki.execute("SELECT COUNT(*) FROM Doviz WHERE Tarih=? AND Kod=?", (Tarih, Kod))
    if yetki.fetchone()[0] == 0:
        yetki.execute(
            "INSERT INTO Doviz VALUES(?, ?, ?, ?)",
            (Tarih, Ad, Kod, Deger)
        )
    db.commit()
    db.close()

    # Tarih listesini güncelle (tekrar ekleme)
    guncelle_tarih_listesi()


def guncelle_tarih_listesi():
    """trhlist listbox'ını veritabanındaki benzersiz tarihlerle doldurur."""
    trhlist.delete(0, END)
    db = sqlite3.connect("../Doviz.db")
    yetki = db.cursor()
    yetki.execute("SELECT DISTINCT Tarih FROM Doviz ORDER BY Tarih DESC")
    sonuclar = yetki.fetchall()
    db.close()
    for satir in sonuclar:
        trhlist.insert(END, satir[0])


def tarih_secildi(event=None):
    """Tarih listesinden bir tarih seçildiğinde o tarihe ait dövizleri gösterir."""
    secilen_index = trhlist.curselection()
    if not secilen_index:
        return
    secilen_tarih = trhlist.get(secilen_index)

    gecmislstbx.delete(0, END)

    db = sqlite3.connect("../Doviz.db")
    yetki = db.cursor()
    yetki.execute(
        "SELECT Isim, Kod, BirTLKarsiligi FROM Doviz WHERE Tarih = ? ORDER BY Isim",
        (secilen_tarih,)
    )
    sonuclar = yetki.fetchall()
    db.close()

    if sonuclar:
        gecmislstbx.insert(END, f"=== {secilen_tarih} ===")
        for i, satir in enumerate(sonuclar, 1):
            gecmislstbx.insert(END, f"{i}. {satir[0]} ({satir[1]})")
            gecmislstbx.insert(END, f"   1 TL = {satir[2]} {satir[1]}")
    else:
        gecmislstbx.insert(END, "Bu tarihe ait veri bulunamadı.")


def guncel_tl_hesapla():
    """
    Veritabanındaki tüm varlıkların şu anki kur üzerinden toplam TL değerini hesaplar.
    Her varlık: sahip olunan döviz miktarı / şu anki kur (1 TL = X döviz) = TL değeri
    """
    datab = sqlite3.connect("../Varlıklarım.db")
    yetki = datab.cursor()
    yetki.execute("SELECT DovizKodu, Miktari FROM Varliklar")
    varliklar = yetki.fetchall()
    datab.close()

    toplam_guncel_tl = 0.0
    for varlik in varliklar:
        kod = varlik[0]
        miktar = varlik[1]
        # Şu anki API verisinden bu kodun kurunu bul
        for doviz in veriler["result"]["data"]:
            if doviz["code"] == kod:
                guncel_kur = float(doviz["rate"])  # 1 TL = guncel_kur döviz
                if guncel_kur > 0:
                    tl_degeri = miktar / guncel_kur
                    toplam_guncel_tl += tl_degeri
                break

    return toplam_guncel_tl


def dovizsecme():
    """Listbox'tan döviz seçip TL miktarını hesaplar ve varlıklara ekler."""
    secilen_index = dovizadı.curselection()
    if not secilen_index:
        return

    secilen_index_int = secilen_index[0]
    carpilan = float(rate_list[secilen_index_int])

    miktar_str = miktargir.get()
    if not miktar_str.isdigit():
        return

    carpim = carpilan * int(miktar_str)

    code_list = [str(i["code"]) for i in veriler["result"]["data"]]
    kod = code_list[secilen_index_int]
    isim = veriler["result"]["data"][secilen_index_int]["name"]

    yatirilan_tl = int(miktar_str)

    datab = sqlite3.connect("../Varlıklarım.db")
    yetki = datab.cursor()
    yetki.execute("""
        CREATE TABLE IF NOT EXISTS Varliklar(
            DovizKodu TEXT,
            Miktari REAL,
            YatirilanTL INTEGER
        )
    """)
    yetki.execute(
        "INSERT INTO Varliklar VALUES(?, ?, ?)",
        (kod, carpim, yatirilan_tl)
    )
    datab.commit()

    yetki.execute("SELECT SUM(YatirilanTL) FROM Varliklar")
    toplam_yatirilan = yetki.fetchone()[0] or 0
    datab.close()

    eklenen.insert(END, f"{isim} ({kod}): {carpim:.4f}")

    # Şu anki TL değerini hesapla
    guncel_tl = guncel_tl_hesapla()
    fark = guncel_tl - toplam_yatirilan
    fark_str = f"+{fark:.2f}" if fark >= 0 else f"{fark:.2f}"

    varlıklarlst.delete(0, END)
    varlıklarlst.insert(END, f"Toplam yatırılan TL : {toplam_yatirilan:.2f} TL")
    varlıklarlst.insert(END, f"Şu anki TL değeri   : {guncel_tl:.2f} TL")
    varlıklarlst.insert(END, f"Kâr / Zarar         : {fark_str} TL")


def tarihsecme():
    secilen_index2 = trhlist.curselection()
    if secilen_index2:
        return trhlist.get(secilen_index2)
    return None

load_dotenv()
# --- API bağlantısı ---
conn = http.client.HTTPSConnection("api.collectapi.com")
headers = {
    'content-type': "application/json",
    'authorization': os.getenv("API_KEY")
}
conn.request("GET", "/economy/currencyToAll?int=10&base=TRY", headers=headers)
res = conn.getresponse()
data = res.read()
veriler = json.loads(data)

# --- Arayüz ---
pencere = Tk()
pencere.title("Döviz Uygulaması")

trhlbl = Label(pencere, text="Kayıtlı Tarihler")
trhlbl.grid(column=0, row=0, columnspan=2)
trhlist = Listbox(pencere, height=4, width=30, selectmode=SINGLE)
trhlist.grid(column=0, row=1, columnspan=2, padx=5, pady=5)
# Tarih seçildiğinde geçmiş verileri otomatik göster
trhlist.bind("<<ListboxSelect>>", tarih_secildi)

yazi1 = Label(pencere, text="Döviz adı seç")
yazi1.grid(row=2, column=0)
dovizadı = Listbox(pencere, selectmode=SINGLE, width=35)
dovizadı.grid(row=3, column=0, padx=5, pady=5)

secimbtn = Button(pencere, text="Dövizi Seç ve Ekle", command=dovizsecme)
secimbtn.grid(row=4, column=1)

miktarlbl = Label(pencere, text="Kaç TL Yatıracaksın")
miktarlbl.grid(row=2, column=1)
miktargir = Entry(pencere, bg="yellow")
miktargir.grid(row=3, column=1)

eklenenlbl = Label(pencere, text="Eklenenler")
eklenenlbl.grid(row=2, column=2)
eklenen = Listbox(pencere,  width=30)
eklenen.grid(row=3, column=2, padx=5, pady=5)

gecmislbl = Label(pencere, text="Seçilen Tarihteki Veriler")
gecmislbl.grid(row=2, column=3)
gecmislstbx = Listbox(pencere, width=35)
gecmislstbx.grid(row=3, column=3, padx=5, pady=5)

varlıklarlbl = Label(pencere, text="Varlıklarım")
varlıklarlbl.grid(row=2, column=4)
varlıklarlst = Listbox(pencere, width=30)
varlıklarlst.grid(row=3, column=4, padx=5, pady=5)

# --- API verilerini işle ve kaydet ---
rate_list = []
for i in veriler["result"]["data"]:
    dovizadı.insert(END, f"{i['name']} / {i['code']} / {i['rate']}")
    rate_list.append(str(i["rate"]))
    veriTabanı_baslangic(Tarih, i["name"], i["code"], i["rate"])

pencere.mainloop()