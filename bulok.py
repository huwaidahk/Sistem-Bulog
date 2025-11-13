from datetime import datetime

class Supplier:
    def __init__(self, nama_petani, asal_petani, jumlah_karung):
        self.id = id(self)
        self.nama_petani = nama_petani
        self.asal_petani = asal_petani
        self.jumlah_karung = jumlah_karung
        self.created_at = datetime.now()

class GoodType:
    def __init__(self, nama_tipe, description=""):
        self.id = id(self)
        self.nama_tipe = nama_tipe
        self.description = description
        self.created_at = datetime.now()

class Item:
    def __init__(self, tipe: GoodType, jumlah_karung=0, berat_kg=0.0, grade='A'):
        self.id = id(self)
        self.type = tipe
        self.jumlah_karung = jumlah_karung
        self.berat_kg = berat_kg
        self.grade = grade
        self.created_at = datetime.now()

class Warehouse:
    def __init__(self, nama_gudang, alamat=""):
        self.id = id(self)
        self.nama_gudang = nama_gudang
        self.alamat = alamat
        self.employees = []
        self.created_at = datetime.now()

class Employee:
    def __init__(self, nama, warehouse: Warehouse):
        self.id = id(self)
        self.nama = nama
        self.warehouse = warehouse
        warehouse.employees.append(self)
        self.created_at = datetime.now()

class Consumer:
    def __init__(self, nama, alamat=""):
        self.id = id(self)
        self.nama = nama
        self.alamat = alamat
        self.created_at = datetime.now()

class Transaction:
    def __init__(self, jenis, item: Item, jumlah_karung, total_harga=0.0, supplier=None, consumer=None):
        self.id = id(self)
        self.jenis = jenis
        self.item = item
        self.jumlah_karung = jumlah_karung
        self.total_harga = total_harga
        self.supplier = supplier
        self.consumer = consumer
        self.timestamp = datetime.now()
        # Update stok
        if jenis == "masuk":
            item.jumlah_karung += jumlah_karung
        elif jenis == "keluar":
            item.jumlah_karung = max(0, item.jumlah_karung - jumlah_karung)


# ===============================
# STORAGE
# ===============================
suppliers = []
good_types = []
items = []
warehouses = []
consumers = []
transactions = []

# ===============================
# FUNCTIONS
# ===============================

def add_supplier():
    nama = input("Nama Petani: ")
    asal = input("Asal Petani: ")
    jumlah = int(input("Jumlah Karung: "))
    s = Supplier(nama, asal, jumlah)
    suppliers.append(s)
    print("Supplier ditambahkan!")

def list_suppliers():
    print("=== Daftar Supplier ===")
    for s in suppliers:
        print(f"{s.nama_petani} ({s.asal_petani}) - {s.jumlah_karung} karung")

def add_good_type():
    nama = input("Nama Jenis Barang: ")
    desc = input("Deskripsi: ")
    gt = GoodType(nama, desc)
    good_types.append(gt)
    print("Jenis Barang ditambahkan!")

def list_good_types():
    print("=== Jenis Barang ===")
    for gt in good_types:
        print(f"{gt.nama_tipe} - {gt.description}")

def add_item():
    print("Pilih Jenis Barang:")
    for i, gt in enumerate(good_types):
        print(f"{i+1}. {gt.nama_tipe}")
    idx = int(input("Pilihan: ")) - 1
    jumlah = int(input("Jumlah Karung: "))
    berat = float(input("Berat per Karung (kg): "))
    grade = input("Grade (A/B): ")
    it = Item(good_types[idx], jumlah, berat, grade)
    items.append(it)
    print("Item ditambahkan!")

def list_items():
    print("=== Items ===")
    for it in items:
        print(f"{it.type.nama_tipe} - {it.jumlah_karung} karung - {it.berat_kg} kg - Grade {it.grade}")

def add_warehouse():
    nama = input("Nama Gudang: ")
    alamat = input("Alamat: ")
    w = Warehouse(nama, alamat)
    warehouses.append(w)
    print("Gudang ditambahkan!")

def add_employee():
    print("Pilih Gudang:")
    for i, w in enumerate(warehouses):
        print(f"{i+1}. {w.nama_gudang}")
    idx = int(input("Pilihan: ")) - 1
    nama = input("Nama Karyawan: ")
    e = Employee(nama, warehouses[idx])
    print("Karyawan ditambahkan!")

def list_warehouses():
    print("=== Gudang ===")
    for w in warehouses:
        print(f"{w.nama_gudang} ({w.alamat}) - Karyawan: {[e.nama for e in w.employees]}")

def add_consumer():
    nama = input("Nama Konsumen: ")
    alamat = input("Alamat: ")
    c = Consumer(nama, alamat)
    consumers.append(c)
    print("Konsumen ditambahkan!")

def list_consumers():
    print("=== Konsumen ===")
    for c in consumers:
        print(f"{c.nama} ({c.alamat})")

def add_transaction():
    jenis = input("Jenis (masuk/keluar): ")
    print("Pilih Item:")
    for i, it in enumerate(items):
        print(f"{i+1}. {it.type.nama_tipe} - {it.jumlah_karung} karung")
    idx = int(input("Pilihan: ")) - 1
    jumlah = int(input("Jumlah Karung: "))
    total = float(input("Total Harga: "))
    supplier = None
    consumer = None
    if jenis == "masuk":
        print("Pilih Supplier:")
        for i, s in enumerate(suppliers):
            print(f"{i+1}. {s.nama_petani} ({s.asal_petani})")
        sid = int(input("Pilihan: ")) - 1
        supplier = suppliers[sid] if suppliers else None
    elif jenis == "keluar":
        print("Pilih Konsumen:")
        for i, c in enumerate(consumers):
            print(f"{i+1}. {c.nama}")
        cid = int(input("Pilihan: ")) - 1
        consumer = consumers[cid] if consumers else None

    t = Transaction(jenis, items[idx], jumlah, total, supplier, consumer)
    transactions.append(t)
    print("Transaksi dicatat!")

def list_transactions():
    print("=== Transaksi ===")
    for t in transactions:
        s_name = t.supplier.nama_petani if t.supplier else "-"
        c_name = t.consumer.nama if t.consumer else "-"
        print(f"{t.jenis} - {t.item.type.nama_tipe} - {t.jumlah_karung} karung - Total {t.total_harga} - Supplier: {s_name} - Consumer: {c_name} - {t.timestamp}")

# ===============================
# CLI MENU
# ===============================
def menu():
    while True:
        print("\n=== Sistem Bulok ===")
        print("1. Tambah Supplier")
        print("2. Lihat Supplier")
        print("3. Tambah Jenis Barang")
        print("4. Lihat Jenis Barang")
        print("5. Tambah Item")
        print("6. Lihat Item")
        print("7. Tambah Gudang")
        print("8. Tambah Karyawan")
        print("9. Lihat Gudang")
        print("10. Tambah Konsumen")
        print("11. Lihat Konsumen")
        print("12. Tambah Transaksi")
        print("13. Lihat Transaksi")
        print("0. Keluar")
        pilih = input("Pilih: ")
        if pilih == "1": add_supplier()
        elif pilih == "2": list_suppliers()
        elif pilih == "3": add_good_type()
        elif pilih == "4": list_good_types()
        elif pilih == "5": add_item()
        elif pilih == "6": list_items()
        elif pilih == "7": add_warehouse()
        elif pilih == "8": add_employee()
        elif pilih == "9": list_warehouses()
        elif pilih == "10": add_consumer()
        elif pilih == "11": list_consumers()
        elif pilih == "12": add_transaction()
        elif pilih == "13": list_transactions()
        elif pilih == "0": break
        else: print("Pilihan tidak valid!")

if __name__ == "__main__":
    menu()
