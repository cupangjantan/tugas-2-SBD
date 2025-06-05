import mysql.connector
import sys
from db import conn, opening
import mahasiswa
import instruktur

def login_mhs():
    cursor = conn.cursor()
    opening("Login Mahasiswa")
    try:
        while True:
            email_user = input("1. Daftar\n0. Back\nMasukkan email: ")
            if email_user == "1":
                daftar_mhs()
                return
            elif email_user == "0":
                return main()
            
            cursor.execute("SELECT id_mahasiswa, nama_mahasiswa FROM mahasiswa WHERE email_mahasiswa = %s", (email_user,))
            hasil = cursor.fetchone()

            if hasil:
                id_mhs = hasil[0]
                nama = hasil[1]
                print(f"Login berhasil! Selamat datang, {nama.capitalize()}!\n")
                mahasiswa.menu_mahasiswa(id_mhs)
                return
            else:
                print("Email tidak ditemukan, silakan coba lagi.")  
    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")
    finally:
        cursor.close()      

def daftar_mhs():
    cursor = conn.cursor()
    opening("Pendaftaran Mahasiswa")
    try:
        while True:
            nama = input("Masukkan nama lengkap : ")
            while True:
                email = input("Masukkan email : ")
                cursor.execute("SELECT 1 FROM mahasiswa WHERE email_mahasiswa = %s", (email,))
                cek_email = cursor.fetchone()
                if cek_email:
                    print("Email sudah terdaftar. Silakan gunakan email lain.")
                else:
                    break
            prodi = input("Program studi : ")

            if not nama or not email or not prodi:
                print("Semua field harus diisi. Silakan coba lagi.")
                continue

            cursor.execute("INSERT INTO mahasiswa (nama_mahasiswa, email_mahasiswa, program_studi) VALUES (%s, %s, %s)", (nama, email, prodi))
            conn.commit()
            print("Pendaftaran berhasil! Silakan login.\n")
            return login_mhs()

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")
    finally:
        cursor.close()
        
def login_ins():
    cursor = conn.cursor()
    opening("Login Instruktur")
    try:
        while True:
            email_user = input("1. Daftar\n0. Back\nMasukkan email: ")
            if email_user == "1":
                daftar_ins()
                return
            elif email_user == "0":
                return main()
            
            cursor.execute("SELECT id_instruktur, Nama_Instruktur FROM instruktur WHERE Email_Instruktur = %s", (email_user,))
            hasil = cursor.fetchone()

            if hasil:
                id_ins = hasil[0]
                nama = hasil[1]
                print(f"Login berhasil! Selamat datang Bapak/Ibu {nama.capitalize()}!")
                instruktur.menu_instruktur(id_ins)
                return
            else:
                print("Email tidak ditemukan, silakan coba lagi atau daftar baru.")  
                
    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")
    finally:
        cursor.close() 

def daftar_ins():
    cursor = conn.cursor()
    opening("Pendaftaran Instruktur")
    try:
        while True:
            nama = input("Masukkan nama lengkap : ")
            while True:
                email = input("Masukkan email : ")
                cursor.execute("SELECT 1 FROM instruktur WHERE Email_Instruktur = %s", (email,))
                cek_email = cursor.fetchone()
                if cek_email:
                    print("Email sudah terdaftar. Silakan gunakan email lain.")
                else:
                    break
            bidang = input("Bidang Keahlian : ")

            if not nama or not email or not bidang:
                print("Semua field harus diisi. Silakan coba lagi.")
                continue

            cursor.execute("INSERT INTO instruktur (Nama_Instruktur, Email_Instruktur, Bidang_keahlian) VALUES (%s, %s, %s)", (nama, email, bidang))
            conn.commit()
            print("Pendaftaran berhasil! Silakan login.\n")
            return login_ins()

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan: {err}")
    finally:
        cursor.close()     

def main():
    while True:
        opening("selamat datang kurus python dasar")
        print("1. Mahasiswa")
        print("2. Instruktur")
        print("0. Exit")
    
        pilihan = input("Login sebagai : ").lower()
        if pilihan == "1" or pilihan == "mahasiswa":
            login_mhs()
        elif pilihan == "2" or pilihan == "instruktur":
            login_ins()
        elif pilihan == "0" or pilihan == "exit":
            print("Terima kasih dan Sampai jumpa!")
            conn.close()
            print("Program dihentikan. Sampai jumpa :)")
            sys.exit()  
        else:
            print("Pilihan tidak valid, silakan coba lagi.")
            continue

if __name__ == "__main__":
    main()