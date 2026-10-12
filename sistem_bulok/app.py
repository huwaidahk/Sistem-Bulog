from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, Supplier, GoodType, Item, Warehouse, Employee, Consumer, Transaction
from forms import SupplierForm, GoodTypeForm, ItemForm, WarehouseForm, ConsumerForm, TransactionForm
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Create tables and seed data if empty
@app.before_first_request
def create_tables_and_seed():
    db.create_all()
    # check if there are any suppliers; if none, seed demo data
    if Supplier.query.first() is None:
        seed_demo()

def seed_demo():
    # Suppliers (Rafif)
    s1 = Supplier(nama_petani='Budi', asal_petani='Demak', jumlah_karung=20)
    s2 = Supplier(nama_petani='Siti', asal_petani='Sragen', jumlah_karung=15)
    s3 = Supplier(nama_petani='Tono', asal_petani='Grobogan', jumlah_karung=25)
    db.session.add_all([s1,s2,s3])

    # Good types and items (Anin)
    gt1 = GoodType(nama_tipe='IR64', description='Beras IR64 kualitas umum')
    gt2 = GoodType(nama_tipe='Pandan Wangi', description='Beras wangi, aroma pandan')
    gt3 = GoodType(nama_tipe='Rojolele', description='Beras pulen lokal')
    db.session.add_all([gt1,gt2,gt3])
    db.session.flush()  # get IDs

    i1 = Item(tipe_id=gt1.id, berat_kg=50, jumlah_karung=100, grade='A')
    i2 = Item(tipe_id=gt2.id, berat_kg=50, jumlah_karung=80, grade='B')
    i3 = Item(tipe_id=gt3.id, berat_kg=50, jumlah_karung=120, grade='A')
    db.session.add_all([i1,i2,i3])

    # Warehouses and employees (Huwaidah)
    w1 = Warehouse(nama_gudang='Gudang Utama', alamat='Jl. Raya No.1')
    w2 = Warehouse(nama_gudang='Gudang Depok', alamat='Jl. Depok Dalam II No.5')
    db.session.add_all([w1,w2])
    db.session.flush()

    e1 = Employee(nama_karyawan='Pak Joko', role='penanggung jawab', warehouse_id=w1.id)
    e2 = Employee(nama_karyawan='Bu Rina', role='penanggung jawab', warehouse_id=w2.id)
    db.session.add_all([e1,e2])

    # Consumers (Rafif)
    c1 = Consumer(nama='Toko Berkah', alamat='Pasar 1')
    c2 = Consumer(nama='Warung Maju', alamat='Pasar 2')
    db.session.add_all([c1,c2])
    db.session.flush()

    # Transactions (Rafly)
    t1 = Transaction(jenis='masuk', supplier_id=s1.id, item_id=i1.id, jumlah_karung=20, total_harga=1000000, timestamp=datetime.utcnow())
    t2 = Transaction(jenis='keluar', consumer_id=c1.id, item_id=i1.id, jumlah_karung=50, total_harga=2500000, timestamp=datetime.utcnow())
    db.session.add_all([t1,t2])

    db.session.commit()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    transaksi_today = Transaction.query.filter(db.func.date(Transaction.timestamp) == datetime.utcnow().date()).count()
    transaksi_month = Transaction.query.filter(db.extract('month', Transaction.timestamp) == datetime.utcnow().month).count()
    transaksi_year = Transaction.query.filter(db.extract('year', Transaction.timestamp) == datetime.utcnow().year).count()
    suppliers = Supplier.query.all()
    goodtypes = GoodType.query.all()
    warehouses = Warehouse.query.all()
    consumers = Consumer.query.all()
    items = Item.query.all()
    return render_template('dashboard.html',
                           transaksi_today=transaksi_today,
                           transaksi_month=transaksi_month,
                           transaksi_year=transaksi_year,
                           suppliers=suppliers,
                           goodtypes=goodtypes,
                           warehouses=warehouses,
                           consumers=consumers,
                           items=items)

# Suppliers CRUD (Rafif)
@app.route('/suppliers')
def suppliers_view():
    suppliers = Supplier.query.order_by(Supplier.created_at.desc()).all()
    form = SupplierForm()
    return render_template('suppliers.html', suppliers=suppliers, form=form)

@app.route('/suppliers', methods=['GET', 'POST'])
def suppliers():
    form = SupplierForm()
    if form.validate_on_submit():
        new_supplier = Supplier(
            nama_petani=form.nama_petani.data,
            asal_petani=form.asal_petani.data,
            jumlah_karung=form.jumlah_karung.data
        )
        db.session.add(new_supplier)
        db.session.commit()
        flash('Data supplier berhasil ditambahkan!', 'success')
        return redirect(url_for('suppliers'))
    else:
        if form.errors:
            print("Validasi gagal:", form.errors)

    suppliers = Supplier.query.all()
    return render_template('suppliers.html', form=form, suppliers=suppliers)


# Goods (types) CRUD (Anin)
@app.route('/goods', methods=['GET', 'POST'])
def goods():
    form = GoodTypeForm()
    if form.validate_on_submit():
        new_good = GoodType(
            nama_tipe=form.nama_tipe.data,
            description=form.description.data
        )
        db.session.add(new_good)
        db.session.commit()
        flash('Tipe beras berhasil ditambahkan!', 'success')
        return redirect(url_for('goods'))
    else:
        if form.errors:
            print(" Validasi gagal:", form.errors)

    goods = GoodType.query.order_by(GoodType.nama_tipe).all()
    return render_template('goods.html', form=form, goods=goods)


@app.route('/goods/create', methods=['POST'])
def create_goodtype():
    form = GoodTypeForm()
    if form.validate_on_submit():
        gt = GoodType(nama_tipe=form.nama_tipe.data, description=form.description.data)
        db.session.add(gt)
        db.session.commit()
        flash('Tipe beras ditambahkan', 'success')
    else:
        flash('Validasi gagal', 'danger')
    return redirect(url_for('goods_view'))

# Items CRUD (barang) (Anin)
@app.route('/items', methods=['GET', 'POST'])
def items_view():
    form = ItemForm()

    # isi choices tipe barang & gudang
    form.tipe_id.choices = [(t.id, t.nama_tipe) for t in GoodType.query.order_by(GoodType.nama_tipe).all()]
    warehouse_choices = [(0, '-- Pilih Gudang --')] + [(w.id, w.nama_gudang) for w in Warehouse.query.order_by(Warehouse.nama_gudang).all()]
    form.warehouse_id.choices = warehouse_choices

    # filter grade via query param
    filter_grade = request.args.get('grade', '')

    query = Item.query
    if filter_grade:
        query = query.filter(Item.grade == filter_grade)

    items = query.order_by(Item.created_at.asc()).all()

    if form.validate_on_submit():
        warehouse_id = form.warehouse_id.data if form.warehouse_id.data != 0 else None
        new_item = Item(
            tipe_id=form.tipe_id.data,
            berat_kg=form.berat_kg.data or 0.0,
            jumlah_karung=form.jumlah_karung.data,
            grade=form.grade.data or 'A',
            warehouse_id=warehouse_id
        )
        db.session.add(new_item)
        db.session.commit()
        flash('Item berhasil ditambahkan!', 'success')
        return redirect(url_for('items_view'))

    return render_template('items.html', form=form, items=items, filter_grade=filter_grade)

@app.route('/items/create', methods=['POST'])
def create_item():
    form = ItemForm()
    form.tipe_id.choices = [(t.id, t.nama_tipe) for t in GoodType.query.all()]
    warehouse_choices = [(0, '-- Pilih Gudang --')] + [(w.id, w.nama_gudang) for w in Warehouse.query.order_by(Warehouse.nama_gudang).all()]
    form.warehouse_id.choices = warehouse_choices

    if form.validate_on_submit():
        warehouse_id = form.warehouse_id.data if form.warehouse_id.data != 0 else None
        it = Item(
            tipe_id=form.tipe_id.data,
            berat_kg=form.berat_kg.data or 0.0,
            jumlah_karung=form.jumlah_karung.data,
            grade=form.grade.data or 'A',
            warehouse_id=warehouse_id
        )
        db.session.add(it)
        db.session.commit()
        flash('Item ditambahkan', 'success')
    else:
        flash('Validasi gagal', 'danger')
    return redirect(url_for('items_view'))


# Warehouses CRUD (Huwaidah)
@app.route('/warehouses')
def warehouses_view():
    warehouses = Warehouse.query.order_by(Warehouse.created_at.desc()).all()
    form = WarehouseForm()
    return render_template('warehouses.html', warehouses=warehouses, form=form)


@app.route('/warehouses/create', methods=['POST'])
def create_warehouse():
    form = WarehouseForm()
    if form.validate_on_submit():
        w = Warehouse(
            nama_gudang=form.nama_gudang.data,
            alamat=form.alamat.data,
            penanggung_jawab=form.penanggung_jawab.data  
        )
        db.session.add(w)
        db.session.commit()
        flash('Gudang berhasil ditambahkan!', 'success')
    else:
        flash('Validasi gagal', 'danger')
    return redirect(url_for('warehouses_view'))

# Consumers CRUD (Rafif)
@app.route('/consumers', methods=['GET', 'POST'])
def consumers_view():
    form = ConsumerForm()
    if form.validate_on_submit():
        c = Consumer(nama=form.nama.data, alamat=form.alamat.data)
        db.session.add(c)
        db.session.commit()
        flash('Konsumen berhasil ditambahkan!', 'success')
        return redirect(url_for('consumers_view'))
    else:
        if form.errors:
            print("Validasi gagal:", form.errors)

    consumers = Consumer.query.order_by(Consumer.created_at.desc()).all()
    return render_template('consumers.html', consumers=consumers, form=form)


# Transactions (Rafly)
@app.route('/transactions', methods=['GET', 'POST'])
def transactions_view():
    form = TransactionForm()

    # Populate choices
    form.item_id.choices = [(it.id, f"{it.type.nama_tipe if it.type else 'Item-'+str(it.id)} (stok: {it.jumlah_karung})") for it in Item.query.all()]
    supplier_choices = [(0, '--')] + [(s.id, f"{s.nama_petani} ({s.asal_petani})") for s in Supplier.query.all()]
    consumer_choices = [(0, '--')] + [(c.id, c.nama) for c in Consumer.query.all()]
    form.supplier_id.choices = supplier_choices
    form.consumer_id.choices = consumer_choices

    if form.validate_on_submit():
        jenis = form.jenis.data
        item_id = form.item_id.data
        jumlah = form.jumlah_karung.data
        total = form.total_harga.data or 0.0
        supplier_id = form.supplier_id.data if form.supplier_id.data != 0 else None
        consumer_id = form.consumer_id.data if form.consumer_id.data != 0 else None

        tx = Transaction(
            jenis=jenis,
            item_id=item_id,
            jumlah_karung=jumlah,
            total_harga=total,
            supplier_id=supplier_id,
            consumer_id=consumer_id
        )
        db.session.add(tx)

        # Update stok item
        item = Item.query.get(item_id)
        if item:
            if jenis == 'masuk':
                item.jumlah_karung += jumlah
            else:
                item.jumlah_karung = max(0, item.jumlah_karung - jumlah)

        db.session.commit()
        flash('Transaksi berhasil dicatat', 'success')
        return redirect(url_for('transactions_view'))

    # Jika GET atau validasi gagal
    transactions = Transaction.query.order_by(Transaction.timestamp.asc()).limit(200).all()
    return render_template('transactions.html', transactions=transactions, form=form)

if __name__ == '__main__':
    # Allow running directly. Ensure DATABASE_URL env var can override connection
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
