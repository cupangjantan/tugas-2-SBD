from main import opening, conn
import mysql.connector
from datetime import datetime, date

def profil_mhs(id_mhs):
    cursor = conn.cursor()
    opening("Profil Mahasiswa")
    try:
        cursor.execute("SELECT nama_mahasiswa, email_mahasiswa, program_studi FROM mahasiswa WHERE id_mahasiswa = %s", (id_mhs,))
        hasil = cursor.fetchone()
        
        if hasil:
            nama, email, prodi = hasil
            print(f"Nama\t: {nama} |Email\t: {email}")
            print(f"Program Studi: {prodi}")
            print("====================================")
            cursor.execute(
                "SELECT k.Nama_Kursus, md.periode, md.nilai, md.id_kursusFK FROM mendaftar md JOIN kursus k ON md.id_kursusFK = k.ID_Kursus WHERE id_mhsFK = %s; ", (id_mhs,)
            )
            hasil = cursor.fetchall()
            for i, (nama_kursus, periode, nilai, id_krs) in enumerate(hasil, start=1):
                print(f"{i}. {nama_kursus}({id_krs}) | Periode: {periode} | Nilai: {nilai}")
            if not hasil:
                print("Belum ada kursus yang diambil.\nSilakan daftar kursus di menu kursus.")
        else:
            print("Data mahasiswa tidak ditemukan.")
        print("====================================\n")

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")
    finally:
        cursor.close()

def kursus_mhs(id_mhs):
    while True:
        cursor = conn.cursor(buffered=True)
        opening("Menu Kursus Mahasiswa")
        print("1. Lihat Kursus")
        print("2. Daftar Kursus")
        print("3. Keluar kursus")
        print("0. Back")
        pilihan = input("Masukkan pilihan: ").lower().strip()
        try:
            if pilihan == "1" or pilihan == "lihat kursus":
                cursor.execute("SELECT k.ID_Kursus, k.Nama_Kursus, k.Daya_Tampung, i.Nama_Instruktur FROM mengampu mp JOIN kursus k ON mp.id_kursus = k.ID_Kursus JOIN instruktur i ON mp.id_instruktur = i.ID_Instruktur ORDER BY k.ID_Kursus")
                hasil = cursor.fetchall()
                if hasil:
                    print("=========================================================================")
                    for id_kursus, nama_kursus, daya_tampung, Instruktur in hasil:
                        print(f"{id_kursus}| {nama_kursus} ({daya_tampung})\t| Instruktur: {Instruktur}")
                else:
                    print("Tidak ada kursus yang tersedia untuk didaftar.")
                print("=========================================================================\n\n")

            elif pilihan == "2" or pilihan == "daftar kursus":
                while True:
                    id_kursus = input("Masukkan ID Kursus yang ingin didaftar: ")
                    cursor.execute("SELECT Nama_Kursus FROM kursus WHERE Daya_Tampung > (SELECT count(*) FROM mendaftar WHERE id_kursusFK = %s)", (id_kursus,))
                    cek = cursor.fetchone()

                    if cek:
                        tanggal = datetime.now()
                        nilai = 0
                        periode = input("Ambil periode [Bulan]: ")
                        cursor.execute("INSERT INTO mendaftar (tanggal_mulai, periode, nilai, id_kursusFK, id_mhsFK) VALUES (%s, %s, %s, %s, %s)", (tanggal, periode, nilai, id_kursus, id_mhs))
                        conn.commit()
                        print("Berhasil mendaftar kursus.")
                        break
                    else:
                        print("Mohon maaf, kursus ini sudah penuh.\n")
                    
            elif pilihan == "3" or pilihan == "keluar kursus":
                while True:
                    id_kursus = input("Masukkan ID Kursus : ")
                    cursor.execute("SELECT 1 FROM mendaftar WHERE id_kursusFK = %s AND id_mhsFK = %s", (id_kursus, id_mhs))
                    hasil = cursor.fetchone()
                    if not hasil:
                        print("Anda tidak terdaftar di kursus ini.")
                        continue
                    else:
                        cursor.execute("DELETE FROM mendaftar WHERE id_kursusFK = %s AND id_mhsFK = %s", (id_kursus, id_mhs))
                        conn.commit()
                        print("Berhasil keluar dari kursus.\n")
                        break

            elif pilihan == "0" or pilihan == "back":
                cursor.close()
                break

        except mysql.connector.Error as err:
            print(f"Terjadi kesalahan: {err}")
        finally:
            cursor.close()

def menu_mahasiswa(id_mhs):
    while True:
        opening("Menu Mahasiswa")
        print("1. Profil")
        print("2. Kursus")
        print("0. Back")    
        pilihan = input("Masukkan pilihan: ").lower().strip()
        if pilihan == "1" or pilihan == "profil":
            profil_mhs(id_mhs)
        elif pilihan == "2" or pilihan == "kursus":
            kursus_mhs(id_mhs)
        elif pilihan == "0" or pilihan == "back":
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")


# masih unread result found saat insert di mendaftar
# Perbaiki masalah unread result found saat insert di mendaftar