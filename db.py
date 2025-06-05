import mysql.connector
import sys
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='kursus'
)

if conn.is_connected():
    print('Koneksi berhasil!')
else:
    print('Koneksi gagal!')
    sys.exit() 


def opening(text: str):
    batas = "=" * (len(text) + 6)
    print(f"{batas}\n== {text.upper()} ==\n{batas}")