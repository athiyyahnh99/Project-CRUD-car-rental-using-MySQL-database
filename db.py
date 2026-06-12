# ===================================
# db.py — Konfigurasi & Koneksi Database
# ===================================

import pymysql
from pymysql import cursors, connect


DB_CONFIG = {
    "host":        "localhost",
    "user":        "root",        
    "password":    "Kenzokutowa108",      
    "database":    "rental_mobil",
    "cursorclass": cursors.DictCursor
}


class Database:
    """Mengelola koneksi ke MySQL."""

    @staticmethod
    def get_connection():
        """Buat dan kembalikan koneksi MySQL."""
        try:
            conn = connect(**DB_CONFIG)
            return conn
        except pymysql.Error as e:
            print(f"[ERROR] Gagal konek ke database: {e}")
            return None

    @staticmethod
    def init_db():
        """Buat database, tabel, dan isi data awal jika belum ada."""
        try:
            # Konek tanpa database dulu
            conn = connect(
                host=DB_CONFIG["host"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                cursorclass=cursors.DictCursor
            )

            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
                    cursor.execute(f"USE {DB_CONFIG['database']}")

                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS mobil (
                            id            INT AUTO_INCREMENT PRIMARY KEY,
                            merk          VARCHAR(100) NOT NULL,
                            model         VARCHAR(100) NOT NULL,
                            license_plate VARCHAR(20)  NOT NULL UNIQUE,
                            daily_rate    INT          NOT NULL,
                            availability  BOOLEAN      NOT NULL DEFAULT TRUE
                        )
                    """)

                    cursor.execute("SELECT COUNT(*) as total FROM mobil")
                    if cursor.fetchone()["total"] == 0:
                        seed_data = [
                            ("toyota",     "avanza",  "B 1234 EFT", 500000, True),
                            ("honda",      "brio",    "B 5155 ENT", 300000, True),
                            ("mitsubishi", "xpander", "B 8105 EAS", 700000, True),
                            ("daihatsu",   "sigra",   "B 7865 UAI", 550000, False),
                        ]
                        cursor.executemany(
                            "INSERT INTO mobil (merk, model, license_plate, daily_rate, availability) VALUES (%s,%s,%s,%s,%s)",
                            seed_data
                        )
                        print("[INFO] Data awal berhasil ditambahkan.")

                conn.commit()

            print("[INFO] Database siap digunakan.\n")

        except pymysql.Error as e:
            print(f"[ERROR] Inisialisasi database gagal: {e}")
            exit(1)
