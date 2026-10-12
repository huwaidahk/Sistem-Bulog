from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Rafif
class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    nama_petani = db.Column(db.String(120), nullable=False)
    asal_petani = db.Column(db.String(120), nullable=False)
    jumlah_karung = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    transactions = db.relationship('Transaction', backref='supplier', lazy=True)

    def __repr__(self):
        return f"<Supplier {self.nama_petani}>"

# Anin
class GoodType(db.Model):
    __tablename__ = 'good_types'
    id = db.Column(db.Integer, primary_key=True)
    nama_tipe = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relasi ke Item via backref 'type' di Item
    def __repr__(self):
        return f"<GoodType {self.nama_tipe}>"

# Huwaidah
class Warehouse(db.Model):
    __tablename__ = 'warehouses'
    id = db.Column(db.Integer, primary_key=True)
    nama_gudang = db.Column(db.String(120), nullable=False)
    alamat = db.Column(db.String(255))
    penanggung_jawab = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    employees = db.relationship('Employee', backref='warehouse', lazy=True)
    items = db.relationship('Item', backref='warehouse', lazy=True)

    def __repr__(self):
        return f"<Warehouse {self.nama_gudang}>"

# Anin
class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    tipe_id = db.Column(db.Integer, db.ForeignKey('good_types.id'), nullable=False)
    berat_kg = db.Column(db.Float, default=0.0)
    jumlah_karung = db.Column(db.Integer, default=0)
    grade = db.Column(db.String(10), default='A')
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi ke GoodType (tipe barang)
    type = db.relationship('GoodType', backref=db.backref('items', lazy=True))

    # Relasi ke transaksi (jika sudah ada)
    transactions = db.relationship('Transaction', backref='item', lazy=True)

    def __repr__(self):
        return f"<Item tipe={self.type.nama_tipe if self.type else 'N/A'} karung={self.jumlah_karung} gudang={self.warehouse.nama_gudang if self.warehouse else 'N/A'}>"

# Huwaidah
class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    nama_karyawan = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), default='penanggung jawab')
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))

    def __repr__(self):
        return f"<Employee {self.nama_karyawan}>"

# Rafif
class Consumer(db.Model):
    __tablename__ = 'consumers'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(120), nullable=False)
    alamat = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    transactions = db.relationship('Transaction', backref='consumer', lazy=True)

    def __repr__(self):
        return f"<Consumer {self.nama}>"

#Rafly
class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    jenis = db.Column(db.String(10), nullable=False)  # 'masuk' atau 'keluar'
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=True)
    consumer_id = db.Column(db.Integer, db.ForeignKey('consumers.id'), nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    jumlah_karung = db.Column(db.Integer, nullable=False)
    total_harga = db.Column(db.Float, default=0.0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Transaction {self.jenis} {self.jumlah_karung} karung>"
