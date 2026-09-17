import sqlite3


def komutlari_goster():
    """Kullanıcıya menüdeki komutların ne işe yaradığını tek seferde açıklar."""
    print("\nKomutlar:")
    print("1. Not Ekle -> Yeni bir not başlığı ve içeriği ekler.")
    print("2. Notları Göster -> Kayıtlı tüm notları listeler.")
    print("3. Not Sil -> Belirtilen ID'ye sahip notu siler.")
    print("4. Çıkış -> Uygulamadan çıkar.")


def tablo_olustur():
    """Veritabanı tablosunu varsa oluşturur; notların saklanmasını sağlar."""
    baglanti = sqlite3.connect("notlar.db")
    cursor = baglanti.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS notlar (id INTEGER PRIMARY KEY, baslik TEXT, icerik TEXT)"
    )
    baglanti.commit()
    baglanti.close()


def sonraki_id_al():
    """Son notun ID'sine göre bir sonraki ID'yi hesaplar; böylece 0'dan başlar."""
    baglanti = sqlite3.connect("notlar.db")
    cursor = baglanti.cursor()
    cursor.execute("SELECT MAX(id) FROM notlar")
    max_id = cursor.fetchone()[0]
    baglanti.close()
    return 0 if max_id is None else max_id + 1


def not_ekle(baslik, icerik):
    """Kullanıcıdan alınan başlık ve içeriği veritabanına ekler."""
    tablo_olustur()
    baglanti = sqlite3.connect("notlar.db")
    cursor = baglanti.cursor()

    yeni_id = sonraki_id_al()
    cursor.execute(
        "INSERT INTO notlar (id, baslik, icerik) VALUES (?, ?, ?)",
        (yeni_id, baslik, icerik),
    )

    baglanti.commit()
    print(f"Not eklendi. ID: {yeni_id}")
    baglanti.close()


def notlari_goster():
    """Kayıtlı tüm notları düzenli bir şekilde, görsel olarak daha okunabilir biçimde gösterir."""
    baglanti = sqlite3.connect("notlar.db")
    cursor = baglanti.cursor()
    cursor.execute("SELECT * FROM notlar ORDER BY id")
    notlar = cursor.fetchall()
    baglanti.close()

    if notlar:
        print("\n=== KAYITLI NOTLAR ===")
        for not_ in notlar:
            print(f"\nID: {not_[0]}")
            print(f"Başlık: {not_[1]}")
            print(f"İçerik: {not_[2]}")
            print("----------------------")
    else:
        print("Hiç not bulunamadı.")


def notlari_yeniden_numarala():
    """Silme sonrası kalan notları tekrar 0'dan başlayacak şekilde numaralandırır."""
    baglanti = sqlite3.connect("notlar.db")
    cursor = baglanti.cursor()
    cursor.execute("SELECT id, baslik, icerik FROM notlar ORDER BY id")
    notlar = cursor.fetchall()

    cursor.execute("DELETE FROM notlar")
    for yeni_id, (_, baslik, icerik) in enumerate(notlar):
        cursor.execute(
            "INSERT INTO notlar (id, baslik, icerik) VALUES (?, ?, ?)",
            (yeni_id, baslik, icerik),
        )

    baglanti.commit()
    baglanti.close()


def not_sil(not_id):
    """Belirtilen ID'ye sahip notu veritabanından siler ve ID'leri yeniden düzenler."""
    baglanti = sqlite3.connect("notlar.db")
    cursor = baglanti.cursor()
    cursor.execute("DELETE FROM notlar WHERE id = ?", (int(not_id),))

    if cursor.rowcount > 0:
        baglanti.commit()
        baglanti.close()
        print("Not silindi.")
        notlari_yeniden_numarala()
    else:
        baglanti.close()
        print("Belirtilen ID'ye sahip not bulunamadı.")


if __name__ == "__main__":
    komutlari_goster()
    while True:
        print("\nNotlar Uygulamasına Hoş Geldiniz!")
        print("1. Not Ekle")
        print("2. Notları Göster")
        print("3. Not Sil")
        print("4. Çıkış")
        secim = input("Seçiminizi yapın (1/2/3/4): ")

        if secim == "1":
            not_baslik = input("Not başlığını girin: ")
            not_icerik = input("Not içeriğini girin: ")
            not_ekle(not_baslik, not_icerik)

        elif secim == "2":
            notlari_goster()

        elif secim == "3":
            print("\nSilmeden önce mevcut notlar: ")
            notlari_goster()
            not_id = input("\nSilmek istediğiniz notun ID'sini girin: ")
            not_sil(not_id)

        elif secim == "4":
            print("Uygulamadan çıkılıyor.")
            break

        else:
            print("Geçersiz seçim. Lütfen 1, 2, 3 veya 4 girin.")
