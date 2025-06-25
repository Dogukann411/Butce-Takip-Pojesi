import matplotlib.pyplot as plt
import pandas as pd
import os

class ButceYonetici:
    def __init__(self, ay, yil):
        self.bakiye = 0
        self.islemler = []
        self.ay = ay.zfill(2)
        self.yil = yil
        self.tarih = f"{self.ay}.{self.yil}"  
    def gelir_ekle(self, miktar, aciklama="Gelir"):
        self.bakiye += miktar
        self.islemler.append(("Gelir", miktar, aciklama))
        print(f"{miktar} TL gelir eklendi.")

    def gider_ekle(self, miktar, aciklama="Gider"):
        if miktar > self.bakiye:
            print("Yetersiz bakiye! Gider eklenemedi.")
            return
        self.bakiye -= miktar
        self.islemler.append(("Gider", miktar, aciklama))
        print(f"{miktar} TL gider eklendi.")

        toplam_gelir = sum(m for t, m, _ in self.islemler if t == "Gelir")
        toplam_gider = sum(m for t, m, _ in self.islemler if t == "Gider")

        if toplam_gelir > 0 and toplam_gider > toplam_gelir * 0.8:
            print("Uyarı: Aylık gideriniz, gelirinizin %80'ini geçti. Çok harcama yaptınız!")

    def bakiye_goster(self):
        print(f"\nGüncel Bakiye: {self.bakiye} TL\n")

    def islemleri_goster(self):
        if not self.islemler:
            print("\nHenüz hiç işlem yok.\n")
            return

        gelir_verisi = [(miktar, aciklama) for t_turu, miktar, aciklama in self.islemler if t_turu == "Gelir"]
        gider_verisi = [(miktar, aciklama) for t_turu, miktar, aciklama in self.islemler if t_turu == "Gider"]

        if gelir_verisi:
            print("\n--- Gelirler ---")
            gelir_df = pd.DataFrame(gelir_verisi, columns=["Tutar", "Açıklama"], index=range(1, len(gelir_verisi)+1))
            print(gelir_df)
        else:
            print("\nGelir bulunamadı.")

        if gider_verisi:
            print("\n--- Giderler ---")
            gider_df = pd.DataFrame(gider_verisi, columns=["Tutar", "Açıklama"], index=range(1, len(gider_verisi)+1))
            print(gider_df)
        else:
            print("\nGider bulunamadı.")

    def gider_pasta_grafigi_goster(self):
        giderler = {}
        for t_turu, miktar, aciklama in self.islemler:
            if t_turu == "Gider":
                if aciklama in giderler:
                    giderler[aciklama] += miktar
                else:
                    giderler[aciklama] = miktar

        if not giderler:
            print("\nGösterilecek gider yok.\n")
            return

        etiketler = list(giderler.keys())
        degerler = list(giderler.values())

        plt.figure(figsize=(8, 6))
        plt.pie(degerler, labels=etiketler, autopct='%1.1f%%', startangle=140)
        plt.title('Gider Dağılımı')
        plt.axis('equal')
        plt.show()

    def giderleri_csvye_yaz(self):
        toplam_gider = sum(miktar for t_turu, miktar, _ in self.islemler if t_turu == "Gider")
        dosya_adi = "aylik_gider_ozeti.csv"
        satir = f"{self.tarih}: {toplam_gider} TL\n"

        if not os.path.exists(dosya_adi):
            with open(dosya_adi, "w", encoding="utf-8") as f:
                f.write("Tarih  Toplam Gider\n")
                f.write(satir)
        else:
            with open(dosya_adi, "a", encoding="utf-8") as f:
                f.write(satir)

def tarih():
    print("Lütfen tarih bilgilerini giriniz:")
    ay = input("Ay: ")
    yil = input("Yıl: ")

    yonetici = ButceYonetici(ay, yil)

    while True:
        print("\n--- Kişisel Finans Yöneticisi ---")
        print("1. Gelir Ekle")
        print("2. Gider Ekle")
        print("3. Bakiye Gör")
        print("4. İşlemleri Gör (Gelir ve Gider Tabloları)")
        print("5. Giderleri Pasta Grafiği ile Gör")
        print("6. Çıkış ve Aylık Gideri Kaydet")

        secim = input("Seçiminiz: ")

        if secim == "1":
            miktar = float(input("Gelir miktarı: "))
            aciklama = input("Açıklama: ")
            yonetici.gelir_ekle(miktar, aciklama)
        elif secim == "2":
            miktar = float(input("Gider miktarı: "))
            aciklama = input("Açıklama: ")
            yonetici.gider_ekle(miktar, aciklama)
        elif secim == "3":
            yonetici.bakiye_goster()
        elif secim == "4":
            yonetici.islemleri_goster()
        elif secim == "5":
            yonetici.gider_pasta_grafigi_goster()
        elif secim == "6":
            yonetici.giderleri_csvye_yaz()
            print("Aylık gider özeti dosyaya kaydedildi. Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")

if __name__ == "__main__":
    tarih()
