from db import opening, conn
import mysql.connector
from datetime import datetime, date

def menu_instruktur(id_ins):
    while True:
        opening("Menu Instruktur")
        print("1. Profil Instruktur")
        print("2. Kursus")
        print("3. Resign")
        print("0. Back")
        pilihan = input("Masukkan pilihan: ").lower().strip()
        print(" ")
        if pilihan == "1" or pilihan == "profil":
            profil_ins(id_ins)
        elif pilihan == "2" or pilihan == "kursus":
            kursus_ins(id_ins)
        elif pilihan == "3" or pilihan == "resign":
            resign_ins(id_ins)
        elif pilihan == "0" or pilihan == "back":
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

def profil_ins(id_ins):
    cursor = conn.cursor()
    opening("Profil Instruktur")
    try:
        cursor.execute("SELECT * FROM instruktur WHERE id_instruktur = %s", (id_ins,))
        hasil = cursor.fetchone()
        if hasil:
            id_ins, nama, email, keahlian = hasil
            print(f"|Nama\t: {nama} |Email: {email}\n|Keahlian: {keahlian}")
            print("="*60)

            cursor.execute(
                "SELECT k.Nama_Kursus, mp.peran, mp.gaji FROM mengampu mp JOIN kursus k ON mp.id_kursus = k.ID_Kursus WHERE id_instruktur = %s; ", (id_ins,)
            )
            hasil2 = cursor.fetchall()
            for i, (nama_kursus, peran, gaji) in enumerate(hasil2, start=1):
                print(f"{i}. {nama_kursus} | Peran: {peran} | Gaji: {gaji}")
            if not hasil2:
                print("Belum ada kursus yang diampu.\nSilakan daftar kursus di menu kursus.")
        else:
            print("Data instruktur tidak ditemukan.")
        print("="*60, "\n\n")

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")
    finally:
        cursor.close()

def kursus_ins(id_ins):
    while True:
        cursor = conn.cursor(buffered=True)
        opening("Menu Kursus Instruktur")
        print("1. Lihat peserta Kursus")
        print("2. Ambil Kursus Baru")
        print("3. Hapus Kursus")
        print("0. Back")
        pilihan = input("Masukkan pilihan: ").lower().strip()

        try:
            if pilihan == "1" or pilihan == "lihat peserta kursus":
                cursor.execute(
                    '''SELECT DISTINCT m.nama_mahasiswa, md.nilai, k.Nama_Kursus 
                    FROM mahasiswa m JOIN mendaftar md ON m.id_mahasiswa = md.id_mhsFK JOIN kursus k ON md.id_kursusFK = k.ID_Kursus
                    JOIN mengampu ma ON k.ID_Kursus = ma.id_kursus
                    JOIN instruktur i ON ma.id_instruktur = i.ID_Instruktur
                    WHERE i.ID_Instruktur = %s''', (id_ins,)
                )
                hasil = cursor.fetchall()
                print("="*60)
                if hasil:
                    for nama_mahasiswa, nilai, nama_kursus in hasil:
                        print(f"{nama_mahasiswa} | Nilai: {nilai} | {nama_kursus}")
                else:
                    print("Belum ada peserta kursus yang mendaftar.")
                print("="*60, "\n\n")

            elif pilihan == "2" or pilihan == "ambil kursus baru":
                while True:
                    id_kursus = input("Masukkan ID Kursus yang ingin diambil: ")
                    cursor.execute('''SELECT 1 FROM kursus k
                                   WHERE k.ID_Kursus IN (SELECT ma.id_kursus 
                                   FROM mengampu ma 
                                   WHERE ma.id_instruktur = %s)''', (id_ins,))
                    
                    cek = cursor.fetchone()
                    if cek:
                        print("Maaf, Anda sudah mengampu kursus ini.\nSilakan pilih kursus lain.")
                        continue

                    peran = input("Peran [Pengajar utama/Asisten]: ").lower().strip()
                    if peran == "pengajar utama":
                        gaji = 500000
                    elif peran == "asisten":
                        gaji = 250000 
                    else:
                        print("Peran tidak valid, silakan pilih antara 'Pengajar utama' atau 'Asisten'.")
                        continue 

                    cursor.execute("INSERT INTO mengampu (id_instruktur, id_kursus, peran, gaji) VALUES (%s, %s, %s, %s)", (id_ins, id_kursus, peran, gaji))
                    conn.commit()
                    print("Kursus berhasil diambil.\n")
                    break

            elif pilihan == "3" or pilihan == "hapus kursus":
                while True:
                    id_kursus = input("Masukkan ID Kursus yang ingin dihapus\n0. Batal   : ")
                    if id_kursus == "0":
                        break

                    cursor.execute("SELECT 1 FROM mengampu WHERE id_instruktur = %s AND id_kursus = %s", (id_ins, id_kursus))
                    cek = cursor.fetchone()
                    if cek:
                        cursor.execute("DELETE FROM mengampu WHERE id_instruktur = %s AND id_kursus = %s", (id_ins, id_kursus))
                        conn.commit()
                        print(f"Kursus dengan kode {id_kursus} berhasil dihapus.\n")
                        break
                    else:
                        print("Kursus tidak ditemukan atau Anda tidak mengampu kursus ini.")
                        continue
            elif pilihan == "0" or pilihan == "back":
                # return menu_instruktur(id_ins)
                break
            else:
                print("Pilihan tidak valid, silakan coba lagi.")

        except mysql.connector.Error as err:
            print(f"Terjadi kesalahan: {err}")
        finally:
            cursor.close()

def resign_ins(id_ins):
    cursor = conn.cursor()
    opening("Resign Instruktur")
    konfirmasi = input("Apakah Anda yakin ingin resign? [ya/tidak]: ").lower()

    if konfirmasi == "ya":
        try:
            cursor.execute("DELETE FROM mengampu WHERE id_instruktur = %s", (id_ins,))
            cursor.execute("DELETE FROM instruktur WHERE id_instruktur = %s", (id_ins,))
            conn.commit()
            print("Anda telah resign. Akun berhasil dihapus.\n")
            return # kembali ke menu utama
        except mysql.connector.Error as err:
            print(f"Terjadi kesalahan: {err}")
    else:
        print("Resign dibatalkan.")
    cursor.close()
