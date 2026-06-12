# ===================================
# models.py — Class Model Data Mobil
# ===================================


class Car:
    """Representasi data satu mobil."""

    def __init__(self, id, merk, model, license_plate, daily_rate, availability):
        self.id            = id
        self.merk          = merk
        self.model         = model
        self.license_plate = license_plate
        self.daily_rate    = daily_rate
        self.availability  = availability

    @staticmethod
    def from_dict(data: dict):
        """Buat objek Car dari dictionary (hasil query MySQL)."""
        return Car(
            id            = data["id"],
            merk          = data["merk"],
            model         = data["model"],
            license_plate = data["license_plate"],
            daily_rate    = data["daily_rate"],
            availability  = data["availability"]
        )

    def to_dict(self) -> dict:
        """Konversi objek Car ke dictionary."""
        return {
            "id":            self.id,
            "merk":          self.merk,
            "model":         self.model,
            "license_plate": self.license_plate,
            "daily_rate":    self.daily_rate,
            "availability":  self.availability
        }

    def __repr__(self):
        status = "Tersedia" if self.availability else "Disewa"
        return (f"Car(id={self.id}, merk={self.merk}, model={self.model}, "
                f"plat={self.license_plate}, tarif={self.daily_rate}, status={status})")
