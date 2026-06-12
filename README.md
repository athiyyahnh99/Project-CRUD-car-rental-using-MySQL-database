# Car Rental Inventory Management System

A comprehensive Python application for managing car rental inventory data with Create, Read, Update, and Delete (CRUD) operations, connected to a MySQL database.

## Business Understanding

This project caters to the **car rental industry**, specifically addressing the need to manage vehicle inventory data efficiently. Accurate and up-to-date car data plays a crucial role in ensuring smooth rental operations, from tracking vehicle availability to managing pricing.

**Benefits:**

* Improved data accuracy and consistency for vehicle records
* Streamlined inventory management processes
* Real-time availability tracking for rental vehicles
* Easy access to vehicle data through an interactive menu
* Data export capability for reporting and analysis

**Target Users:**

This application is designed for **rental staff and inventory managers** within a car rental business to facilitate their daily tasks related to managing vehicle data, such as adding new vehicles, updating availability status, and monitoring the fleet.

---

## Features

* **Create:**
    * Add new car entries with details such as brand, model, license plate, daily rate, and availability status.
    * Validation rules to ensure data integrity (unique license plate, correct plate format, numeric rate).

* **Read:**
    * Display all cars in a formatted table with availability status.
    * Filter cars by availability (available or currently rented).
    * Search cars by brand or model name.

* **Update:**
    * Modify existing car data including brand, model, license plate, daily rate, or availability status.
    * Search car by brand, model, or license plate before updating.
    * Confirmation prompt before saving changes.

* **Delete:**
    * Remove unwanted car records from the system.
    * Confirmation prompt before permanent deletion.

* **Export:**
    * Export car data to CSV format for further analysis.
    * Option to export all cars, only available cars, or only rented cars.
    * Custom filename support.

---

## Tech Stack

* **Language:** Python 3.x
* **Database:** MySQL
* **Libraries:** `pymysql`, `csv`, `re`
* **Architecture:** Class-based, modular structure

---

## Project Structure

```
rental_mobil/
├── main.py          # Main application class (CarApp) and menu logic
├── db.py            # Database configuration and connection (Database class)
├── models.py        # Car data model (Car class)
├── repository.py    # CRUD operations (CarRepository class)
└── README.md
```

---

## Installation

1. **Prerequisites:**
    * Python 3.x
    * MySQL Server
    * pymysql library

2. **Clone the repository:**
    ```bash
    git clone https://github.com/<your-username>/rental-mobil-crud.git
    cd rental-mobil-crud
    ```

3. **Install dependencies:**
    ```bash
    pip install pymysql
    ```

4. **Configure database connection in `db.py`:**
    ```python
    DB_CONFIG = {
        "host":     "localhost",
        "user":     "root",      
        "password": "Kenzokutowa108",           
        "database": "rental_mobil"
    }
    ```

5. **Run the application** (database and table will be created automatically):
    ```bash
    python main.py
    ```

---

## Usage

1. **Run the application:**
    ```bash
    python main.py
    ```

2. **CRUD Operations:**
    * **Create:** Select menu `2` → Add a new car with brand, model, license plate, daily rate, and availability status.
    * **Read:** Select menu `1` → View all cars, filter by availability, or search by brand/model.
    * **Update:** Select menu `4` → Search for a car and update any field.
    * **Delete:** Select menu `3` → Select a car by number and confirm deletion.
    * **Export CSV:** Select menu `5` → Choose data filter and export to a `.csv` file.

---

## Data Model

This project uses a **MySQL relational database** to store car inventory data. The following fields are stored in the `mobil` table:

| Field | Data Type | Description |
|---|---|---|
| `id` | INT (AUTO_INCREMENT) | Unique identifier for each car |
| `merk` | VARCHAR(100) | Car brand (e.g., Toyota, Honda) |
| `model` | VARCHAR(100) | Car model (e.g., Avanza, Brio) |
| `license_plate` | VARCHAR(20) | Unique license plate number |
| `daily_rate` | INT | Rental price per day in Rupiah |
| `availability` | BOOLEAN | True = available, False = currently rented |

---

## Database Setup (Manual)

If you prefer to set up the database manually, run the following SQL:

```sql
CREATE DATABASE IF NOT EXISTS rental_mobil;
USE rental_mobil;

CREATE TABLE IF NOT EXISTS mobil (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    merk          VARCHAR(100) NOT NULL,
    model         VARCHAR(100) NOT NULL,
    license_plate VARCHAR(20)  NOT NULL UNIQUE,
    daily_rate    INT          NOT NULL,
    availability  BOOLEAN      NOT NULL DEFAULT TRUE
);
```

Or export the database dump using:
```bash
mysqldump -u root -p rental_mobil > rental_mobil.sql
```

---

## Contributing

Feel free to open a pull request or submit an issue if you encounter any problems or have suggestions for improvements.
