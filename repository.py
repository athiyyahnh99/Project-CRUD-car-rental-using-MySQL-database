# ===================================
# repository.py — Class CRUD ke MySQL
# ===================================

from db import Database
from models import Car
import csv
import os

class CarRepository:
    """Mengelola semua operasi CRUD mobil ke database MySQL."""

    #  READ 

    def get_all(self, filter_avail=None) -> list:
        """Ambil semua mobil. filter_avail: None=semua, True=tersedia, False=disewa."""
        conn = Database.get_connection()
        if not conn:
            return []

        with conn:
            with conn.cursor() as cursor:
                if filter_avail is None:
                    cursor.execute("SELECT * FROM mobil ORDER BY id")
                else:
                    cursor.execute(
                        "SELECT * FROM mobil WHERE availability = %s ORDER BY id",
                        (filter_avail,)
                    )
                rows = cursor.fetchall()

        return [Car.from_dict(r) for r in rows]

    def search(self, keyword: str) -> list:
        """Cari mobil berdasarkan keyword (merk atau model)."""
        conn = Database.get_connection()
        if not conn:
            return []

        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM mobil WHERE LOWER(merk) LIKE %s OR LOWER(model) LIKE %s ORDER BY id",
                    (f"%{keyword}%", f"%{keyword}%")
                )
                rows = cursor.fetchall()

        return [Car.from_dict(r) for r in rows]

    def find_by(self, field: str, value: str) -> list:
        """Cari mobil berdasarkan field tertentu (merk, model, license_plate)."""
        conn = Database.get_connection()
        if not conn:
            return []

        with conn:
            with conn.cursor() as cursor:
                if field == "license_plate":
                    cursor.execute("SELECT * FROM mobil WHERE license_plate = %s", (value,))
                else:
                    cursor.execute(
                        f"SELECT * FROM mobil WHERE LOWER({field}) = %s",
                        (value.lower(),)
                    )
                rows = cursor.fetchall()

        return [Car.from_dict(r) for r in rows]

    def is_plate_exists(self, license_plate: str, exclude_id: int = None) -> bool:
        """Cek apakah plat nomor sudah terdaftar."""
        conn = Database.get_connection()
        if not conn:
            return False

        with conn:
            with conn.cursor() as cursor:
                if exclude_id:
                    cursor.execute(
                        "SELECT id FROM mobil WHERE license_plate = %s AND id != %s",
                        (license_plate, exclude_id)
                    )
                else:
                    cursor.execute(
                        "SELECT id FROM mobil WHERE license_plate = %s",
                        (license_plate,)
                    )
                result = cursor.fetchone()

        return result is not None

    #  CREATE 

    def add(self, car: Car) -> bool:
        """Tambah mobil baru ke database."""
        conn = Database.get_connection()
        if not conn:
            return False

        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO mobil (merk, model, license_plate, daily_rate, availability) VALUES (%s,%s,%s,%s,%s)",
                    (car.merk, car.model, car.license_plate, car.daily_rate, car.availability)
                )
            conn.commit()

        return True

    #  UPDATE 

    def update_field(self, car_id: int, field: str, value) -> bool:
        """Update satu field pada mobil berdasarkan id."""
        conn = Database.get_connection()
        if not conn:
            return False

        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"UPDATE mobil SET {field} = %s WHERE id = %s",
                    (value, car_id)
                )
            conn.commit()

        return True

    #  DELETE 

    def delete(self, car_id: int) -> bool:
        """Hapus mobil berdasarkan id."""
        conn = Database.get_connection()
        if not conn:
            return False

        with conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM mobil WHERE id = %s", (car_id,))
            conn.commit()

        return True

#  EXPORT CSV 
 
    def export_to_csv(self, filename: str = "data_mobil.csv", filter_avail=None) -> bool:
        """
        Export data mobil dari MySQL ke file CSV.
        filter_avail: None=semua, True=tersedia, False=disewa
        """
        cars = self.get_all(filter_avail=filter_avail)
 
        if not cars:
            print("Tidak ada data untuk diekspor.")
            return False
 
        filepath = os.path.abspath(filename)
 
        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
 
            # Header kolom
            writer.writerow(["ID", "Merk", "Model", "Plat Nomor", "Tarif Harian", "Status"])
 
            # Isi data
            for car in cars:
                writer.writerow([
                    car.id,
                    car.merk,
                    car.model,
                    car.license_plate,
                    car.daily_rate,
                    "Tersedia" if car.availability else "Disewa"
                ])
 
        print(f"Data berhasil diekspor ke: {filepath}")
        print(f"Total: {len(cars)} mobil")
        return True