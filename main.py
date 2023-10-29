import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QComboBox
from PyQt5.QtCore import QTimer

class SayiTahminOyunu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sayı Tahmin Oyunu")
        self.setGeometry(100, 100, 400, 300)

        self.zorluk_seviyeleri = {
            "Kolay": (1, 10, 20),
            "Orta": (1, 20, 30),
            "Zor": (1, 30, 40)
        }

        self.current_zorluk = "Kolay"

        self.sayi = None
        self.deneme_sayisi = 0
        self.kalan_sure = 20

        self.setStyleSheet("background-color: #f0f0f0; font-family: Arial, sans-serif;")

        self.etiket = QLabel("Bir sayı tahmin edin:", self)
        self.etiket.setGeometry(20, 20, 300, 30)

        self.zorluk_secici = QComboBox(self)
        self.zorluk_secici.setGeometry(20, 60, 100, 30)
        self.zorluk_secici.addItems(self.zorluk_seviyeleri.keys())
        self.zorluk_secici.currentTextChanged.connect(self.zorluk_degisti)

        self.giris = QLineEdit(self)
        self.giris.setGeometry(20, 100, 100, 30)

        self.tahmin_dugmesi = QPushButton("🔍 Tahmin Et", self)  # Emoji eklemesi
        self.tahmin_dugmesi.setGeometry(20, 140, 100, 30)
        self.tahmin_dugmesi.setStyleSheet("background-color: #3498db; color: white; border: none; border-radius: 5px;")  # Buton stilini özelleştirme
        self.tahmin_dugmesi.clicked.connect(self.tahmini_kontrol_et)

        self.sonuc_etiket = QLabel("", self)
        self.sonuc_etiket.setGeometry(20, 180, 300, 30)

        self.zaman_kalani_etiket = QLabel("", self)
        self.zaman_kalani_etiket.setGeometry(230, 100, 150, 30)

        self.yeniden_baslat_dugmesi = QPushButton("🔄 Yeniden Başlat", self)  # Emoji eklemesi
        self.yeniden_baslat_dugmesi.setGeometry(20, 220, 100, 30)
        self.yeniden_baslat_dugmesi.setStyleSheet("background-color: #2ecc71; color: white; border: none; border-radius: 5px;")  # Buton stilini özelleştirme
        self.yeniden_baslat_dugmesi.clicked.connect(self.yeni_oyun)

        self.cikis_dugmesi = QPushButton("❌ Çıkış", self)  # Emoji eklemesi
        self.cikis_dugmesi.setGeometry(130, 220, 80, 30)
        self.cikis_dugmesi.setStyleSheet("background-color: #e74c3c; color: white; border: none; border-radius: 5px;")  # Buton stilini özelleştirme
        self.cikis_dugmesi.clicked.connect(self.cikis)

        self.zaman_dongusu = QTimer(self)
        self.zaman_dongusu.timeout.connect(self.zaman_doldu)

        self.yeni_oyun()

    def yeni_oyun(self):
        self.sayi = random.randint(self.zorluk_seviyeleri[self.current_zorluk][0], self.zorluk_seviyeleri[self.current_zorluk][1])
        self.deneme_sayisi = 0
        self.kalan_sure = self.zorluk_seviyeleri[self.current_zorluk][2]
        self.guncel_zaman_kalani_goster()
        self.sonuc_etiket.setText("")
        self.giris.setEnabled(True)
        self.tahmin_dugmesi.setEnabled(True)
        self.zaman_dongusu.start(1000)

        min_val, max_val, time_limit = self.zorluk_seviyeleri[self.current_zorluk]
        self.etiket.setText(f"Bir sayı tahmin edin ({min_val} ile {max_val} arasında):")

    def tahmini_kontrol_et(self):
        tahmin = int(self.giris.text())
        self.deneme_sayisi += 1

        if tahmin == self.sayi:
            self.sonuc_etiket.setText(f"<span style='color: green;'>Tebrikler! {self.deneme_sayisi} denemede {self.sayi} sayısını buldunuz!</span>")
            self.zaman_dongusu.stop()
            self.giris.setEnabled(False)
            self.tahmin_dugmesi.setEnabled(False)
        elif tahmin < self.sayi:
            self.sonuc_etiket.setText(f"<span style='color: red;'>Tahmininiz çok düşük: {tahmin}'dan daha yüksek bir sayı girin</span>")
        else:
            self.sonuc_etiket.setText(f"<span style='color: red;'>Tahmininiz çok yüksek: {tahmin}'dan daha düşük bir sayı girin</span>")

            # İpucu gösterme
            if self.gosterilecek_ipucu < len(self.ipucu_metinleri):
                ipucu = self.ipucu_metinleri[self.gosterilecek_ipucu]
                self.sonuc_etiket.setText(f"<span style='color: orange;'>İpucu: {ipucu}</span>")
                self.gosterilecek_ipucu += 1

    def zaman_doldu(self):
        self.kalan_sure -= 1
        if self.kalan_sure > 0:
            self.guncel_zaman_kalani_goster()
        else:
            self.sonuc_etiket.setText("<span style='color: red;'>Zaman doldu! Tekrar deneyin.</span>")
            self.zaman_dongusu.stop()
            self.giris.setEnabled(False)
            self.tahmin_dugmesi.setEnabled(False)

    def guncel_zaman_kalani_goster(self):
        self.zaman_kalani_etiket.setText(f"Kalan süre: {self.kalan_sure} saniye")

    def cikis(self):
        sys.exit()

    def zorluk_degisti(self, yeni_zorluk):
        self.current_zorluk = yeni_zorluk
        if self.zaman_dongusu.isActive():
            self.zaman_dongusu.stop()
            self.yeni_oyun()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SayiTahminOyunu()
    window.show()
    sys.exit(app.exec_())
