# ===================================
# main.py — Class Aplikasi & Menu Utama
# ===================================
# Developed by. Athiyyah Nisrina Husna

import re
from db import Database
from models import Car
from repository import CarRepository


# ===== Helper Functions =====

def format_rupiah(amount):
    return f"Rp {amount:,.0f}".replace(",", ".")


def print_header(title):
    line = "=" * 60
    print(f"\n{line}")
    print(f"{title}")
    print(line)


def print_car_table(cars: list):
    if not cars:
        print("(Tidak ada data mobil yang ditampilkan)")
        return

    c1, c2, c3, c4, c5, c6 = 4, 12, 10, 14, 14, 12
    border = f"+{'-'*(c1+2)}+{'-'*(c2+2)}+{'-'*(c3+2)}+{'-'*(c4+2)}+{'-'*(c5+2)}+{'-'*(c6+2)}+"
    header = f"| {'No':<{c1}} | {'Merk':<{c2}} | {'Model':<{c3}} | {'Plat Nomor':<{c4}} | {'Tarif/Hari':<{c5}} | {'Status':<{c6}} |"

    print(f"\n{border}")
    print(header)
    print(border)

    for idx, car in enumerate(cars, start=1):
        status = "Tersedia" if car.availability else "Disewa"
        print(
            f"| {idx:<{c1}} "
            f"| {car.merk:<{c2}} "
            f"| {car.model:<{c3}} "
            f"| {car.license_plate:<{c4}} "
            f"| {format_rupiah(car.daily_rate):<{c5}} "
            f"| {status:<{c6}} |"
        )

    print(border)
    print(f"Total: {len(cars)} mobil\n")


# ===== Class Aplikasi =====

class CarApp:
    """Class utama yang mengelola menu dan alur aplikasi."""

    def __init__(self):
        self.repo    = CarRepository()
        self.running = True

    # ————— Menu —————

    def main_menu(self):
        print("\n=== SELAMAT DATANG DI APLIKASI RENTAL MOBIL ===")
        print("Silahkan pilih menu: ")
        print("1. Menampilkan daftar mobil")
        print("2. Menambahkan data mobil baru")
        print("3. Menghapus data mobil")
        print("4. Mengupdate data mobil")
        print("5. Export data ke CSV")
        print("6. Exit aplikasi")
        return input("Masukkan angka menu yang ingin dijalankan: ")

    def sub_menu1(self):
        print("\nPilih Menu: ")
        print("1. Tampilkan daftar semua mobil")
        print("2. Cari mobil berdasarkan nama merk/model")
        print("3. Kembali ke menu utama")
        return input("Masukkan angka menu yang ingin dijalankan: ")

    def sub_menu2(self):
        print("\nPilih Menu: ")
        print("1. Tambahkan data mobil")
        print("2. Kembali ke menu utama")
        return input("Masukkan angka menu yang ingin dijalankan: ")

    def sub_menu3(self):
        print("\nPilih Menu: ")
        print("1. Hapus data mobil")
        print("2. Kembali ke menu utama")
        return input("Masukkan angka menu yang ingin dijalankan: ")

    def sub_menu4(self):
        print("\nPilih Menu: ")
        print("1. Update data mobil")
        print("2. Kembali ke menu utama")
        return input("Masukkan angka menu yang ingin dijalankan: ")

    # ————— CRUD Actions —————

    def view_all(self):
        print_header("DAFTAR SEMUA MOBIL")
        cars = self.repo.get_all()
        print_car_table(cars)

        print("Filter tampilan:")
        print("1. Hanya mobil tersedia")
        print("2. Hanya mobil sedang disewa")
        choose = input("Pilih filter [1/2] atau Enter untuk skip: ").strip()

        if choose == "1":
            print_header("MOBIL TERSEDIA")
            print_car_table(self.repo.get_all(filter_avail=True))
        elif choose == "2":
            print_header("MOBIL SEDANG DISEWA")
            print_car_table(self.repo.get_all(filter_avail=False))
        elif choose == "":
            pass
        else:
            print("\nPilihan tidak valid.")

    def search_car(self):
        print_header("CARI MOBIL")
        keyword = input("Masukkan nama merk atau model mobil yang dicari: ").strip().lower()

        if not keyword:
            print("\nKeyword tidak boleh kosong.")
            return

        result = self.repo.search(keyword)
        print_header(f"HASIL PENCARIAN: {len(result)} mobil ditemukan")
        if result:
            print_car_table(result)
        else:
            print("Tidak ada mobil yang sesuai dengan pencarian Anda.\n")

    def add_car(self):
        print_header("TAMBAH DATA MOBIL")

        while True:
            merk = input("Masukkan merk mobil: ").strip()
            if merk:
                break
            print("Merk tidak boleh kosong!")

        while True:
            model = input("Masukkan model mobil: ").strip()
            if model:
                break
            print("Model tidak boleh kosong!")

        while True:
            license_plate = input("Masukkan plat nomor (contoh: B 1234 ABC): ").strip().upper()
            if not re.fullmatch(r"[A-Z]{1,2} \d{1,4} [A-Z]{1,3}", license_plate):
                print("Format plat tidak valid! Contoh yang benar: B 1234 ABC")
            elif self.repo.is_plate_exists(license_plate):
                print("Plat nomor sudah terdaftar! Masukkan plat nomor lain.")
            else:
                break

        while True:
            daily_rate_input = input("Masukkan tarif harian (Rp): ").strip()
            if daily_rate_input.isdigit():
                daily_rate = int(daily_rate_input)
                break
            print("Tarif harus berupa angka!")

        while True:
            print("Status ketersediaan mobil:")
            print("1. Tersedia")
            print("2. Sedang Disewa")
            avail_input = input("Pilih status (1/2): ").strip()
            if avail_input == "1":
                availability = True
                break
            elif avail_input == "2":
                availability = False
                break
            print("Pilihan tidak valid, masukkan 1 atau 2!")

        new_car = Car(
            id=None,
            merk=merk,
            model=model,
            license_plate=license_plate,
            daily_rate=daily_rate,
            availability=availability
        )

        print(f"\nData baru: {merk} {model} | {license_plate} | {format_rupiah(daily_rate)} | {'Tersedia' if availability else 'Disewa'}")
        confirm = input("Yakin untuk menambah mobil? (y/n): ").strip().lower()

        if confirm == "y":
            if self.repo.add(new_car):
                print("Mobil berhasil ditambahkan!")
                print_car_table(self.repo.get_all())
        else:
            print("Mobil batal ditambahkan.")

    def delete_car(self):
        cars = self.repo.get_all()
        print_car_table(cars)

        while True:
            index_input = input("Masukkan nomor mobil yang ingin dihapus: ").strip()
            if index_input.isdigit():
                index_delete = int(index_input)
                break
            print("Nomor harus berupa angka!")

        if 1 <= index_delete <= len(cars):
            deleted = cars[index_delete - 1]
            print(f"\nMobil yang akan dihapus:")
            print_car_table([deleted])
            confirm = input("Yakin ingin menghapus mobil ini? (y/n): ").strip().lower()

            if confirm == "y":
                if self.repo.delete(deleted.id):
                    print(f"'{deleted.merk} {deleted.model}' berhasil dihapus!")
                    print_car_table(self.repo.get_all())
            else:
                print("Penghapusan dibatalkan.")
        else:
            print("Nomor tidak valid!")

    def update_car(self):
        cars = self.repo.get_all()
        print_car_table(cars)

        while True:
            print("Cari mobil berdasarkan:")
            print("1. Merk")
            print("2. Model")
            print("3. Plat Nomor")
            search_choice = input("Pilih metode pencarian (1-3): ").strip()

            if search_choice == "1":
                keyword = input("Masukkan merk mobil: ").strip()
                result = self.repo.find_by("merk", keyword)
            elif search_choice == "2":
                keyword = input("Masukkan model mobil: ").strip()
                result = self.repo.find_by("model", keyword)
            elif search_choice == "3":
                keyword = input("Masukkan plat nomor: ").strip().upper()
                result = self.repo.find_by("license_plate", keyword)
            else:
                print("Pilihan tidak valid, masukkan 1-3!")
                continue

            if not result:
                print("Mobil tidak ditemukan! Coba lagi.")
                continue

            if len(result) == 1:
                found = result[0]
                break
            else:
                print("\nDitemukan lebih dari 1 mobil:")
                print_car_table(result)
                while True:
                    input_choice = input(f"Pilih nomor mobil (1-{len(result)}): ").strip()
                    if input_choice.isdigit() and 1 <= int(input_choice) <= len(result):
                        found = result[int(input_choice) - 1]
                        break
                    print(f"Pilihan tidak valid! Masukkan 1-{len(result)}.")
                break

        while True:
            print("\nPilih bagian yang ingin diupdate:")
            print("1. Merk")
            print("2. Model")
            print("3. Plat Nomor")
            print("4. Tarif Harian")
            print("5. Status Ketersediaan")
            choices = input("Pilih (1-5): ").strip()

            field, new_value = None, None

            if choices == "1":
                while True:
                    val = input("Masukkan merk baru: ").strip()
                    if val:
                        field, new_value = "merk", val
                        break
                    print("Merk tidak boleh kosong!")
                break

            elif choices == "2":
                while True:
                    val = input("Masukkan model baru: ").strip()
                    if val:
                        field, new_value = "model", val
                        break
                    print("Model tidak boleh kosong!")
                break

            elif choices == "3":
                while True:
                    val = input("Masukkan plat nomor baru (contoh: B 1234 ABC): ").strip().upper()
                    if not re.fullmatch(r"[A-Z]{1,2} \d{1,4} [A-Z]{1,3}", val):
                        print("Format plat tidak valid!")
                    elif self.repo.is_plate_exists(val, exclude_id=found.id):
                        print("Plat nomor sudah terdaftar!")
                    else:
                        field, new_value = "license_plate", val
                        break
                break

            elif choices == "4":
                while True:
                    val = input("Masukkan tarif harian baru (Rp): ").strip()
                    if val.isdigit():
                        field, new_value = "daily_rate", int(val)
                        break
                    print("Tarif harus berupa angka!")
                break

            elif choices == "5":
                while True:
                    print("Status ketersediaan:")
                    print("1. Tersedia")
                    print("2. Sedang Disewa")
                    val = input("Pilih status (1/2): ").strip()
                    if val == "1":
                        field, new_value = "availability", True
                        break
                    elif val == "2":
                        field, new_value = "availability", False
                        break
                    print("Pilihan tidak valid!")
                break

            else:
                print("Pilihan tidak valid, masukkan 1-5!")

        print(f"\nUpdate field '{field}' → {new_value}")
        confirm = input("Yakin ingin menyimpan perubahan? (y/n): ").strip().lower()

        if confirm == "y":
            if self.repo.update_field(found.id, field, new_value):
                print(f"'{found.merk} {found.model}' berhasil diupdate!")
                print_car_table(self.repo.get_all())
        else:
            print("Update dibatalkan.")

    # ————— Export CSV —————

    def export_csv(self):
        print_header("EXPORT DATA KE CSV")

        print("Pilih data yang ingin diekspor:")
        print("1. Semua mobil")
        print("2. Hanya mobil tersedia")
        print("3. Hanya mobil sedang disewa")
        choose = input("Pilih (1-3): ").strip()

        if choose == "1":
            filter_avail = None
            label = "semua"
        elif choose == "2":
            filter_avail = True
            label = "tersedia"
        elif choose == "3":
            filter_avail = False
            label = "disewa"
        else:
            print("Pilihan tidak valid.")
            return

        # Nama file
        default_name = f"data_mobil_{label}.csv"
        filename_input = input(f"Nama file CSV (Enter untuk pakai '{default_name}'): ").strip()
        filename = filename_input if filename_input else default_name

        # Pastikan ekstensi .csv
        if not filename.endswith(".csv"):
            filename += ".csv"

        self.repo.export_to_csv(filename=filename, filter_avail=filter_avail)

    # ————— Main Loop —————

    def run(self):
        while self.running:
            choice = self.main_menu()

            if choice == "1":  # READ
                while True:
                    submenu = self.sub_menu1()
                    if submenu == "1":
                        self.view_all()
                    elif submenu == "2":
                        self.search_car()
                    elif submenu == "3":
                        break
                    else:
                        print("\nPilihan tidak ada di dalam menu\n")

            elif choice == "2":  # CREATE
                while True:
                    submenu = self.sub_menu2()
                    if submenu == "1":
                        self.add_car()
                    elif submenu == "2":
                        break
                    else:
                        print("\nPilihan tidak ada di dalam menu\n")

            elif choice == "3":  # DELETE
                while True:
                    submenu = self.sub_menu3()
                    if submenu == "1":
                        self.delete_car()
                    elif submenu == "2":
                        break
                    else:
                        print("\nPilihan tidak ada di dalam menu\n")

            elif choice == "4":  # UPDATE
                while True:
                    submenu = self.sub_menu4()
                    if submenu == "1":
                        self.update_car()
                    elif submenu == "2":
                        break
                    else:
                        print("\nPilihan tidak ada di dalam menu\n")

            elif choice == "5":  # EXPORT CSV
                self.export_csv()

            elif choice == "6":  # EXIT
                print("Terima kasih telah menggunakan aplikasi rental mobil!")
                self.running = False

            else:
                print("\nPilihan tidak ada di dalam menu\n")


# ===== Entry Point =====

if __name__ == "__main__":
    Database.init_db()
    app = CarApp()
    app.run()