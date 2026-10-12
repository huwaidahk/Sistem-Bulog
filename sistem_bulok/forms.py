from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional

# Rafif
class SupplierForm(FlaskForm):
    nama_petani = StringField('Nama Petani', validators=[DataRequired()])
    asal_petani = StringField('Asal Petani', validators=[DataRequired()])
    jumlah_karung = IntegerField('Jumlah Karung', validators=[DataRequired()])
    submit = SubmitField('Tambah')

# Anin
class GoodTypeForm(FlaskForm):
    nama_tipe = StringField('Nama Tipe Beras', validators=[DataRequired()])
    description = StringField('Deskripsi (opsional)')
    submit = SubmitField('Tambah')

# Anin
class ItemForm(FlaskForm):
    tipe_id = SelectField('Tipe Barang', coerce=int, validators=[DataRequired()])
    berat_kg = FloatField('Berat (kg)', validators=[Optional()])
    jumlah_karung = IntegerField('Jumlah Karung', validators=[DataRequired()])
    grade = StringField('Grade', validators=[Optional()])
    warehouse_id = SelectField('Gudang', coerce=int, validators=[Optional()])
    submit = SubmitField('Tambah Item')

class ItemFilterForm(FlaskForm):
    grade_filter = SelectField(
        "Filter Grade",
        choices=[("", "Semua Grade"), ("A", "Grade A"), ("B", "Grade B")],
        default="",
        render_kw={"class": "form-select"}
    )
    submit_filter = SubmitField("Filter", render_kw={"class": "btn btn-primary"})

# Huwaidah
class WarehouseForm(FlaskForm):
    nama_gudang = StringField('Nama Gudang', validators=[DataRequired()])
    alamat = StringField('Alamat', validators=[Optional()])
    penanggung_jawab = StringField('Penanggung Jawab', validators=[Optional()])  
    submit = SubmitField('Simpan')

# Rafif
class ConsumerForm(FlaskForm):
    nama = StringField('Nama Konsumen', validators=[DataRequired()])
    alamat = StringField('Alamat', validators=[Optional()])
    submit = SubmitField('Simpan')

# Rafly
class TransactionForm(FlaskForm):
    jenis = SelectField('Jenis', choices=[('masuk','Masuk'),('keluar','Keluar')], validators=[DataRequired()])
    item_id = SelectField('Item', coerce=int, validators=[DataRequired()])
    jumlah_karung = IntegerField('Jumlah Karung', validators=[DataRequired()])
    total_harga = FloatField('Total Harga', validators=[Optional()])
    supplier_id = SelectField('Supplier', coerce=int, validators=[Optional()])
    consumer_id = SelectField('Consumer', coerce=int, validators=[Optional()])
    submit = SubmitField('Simpan')

