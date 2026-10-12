import os 

# Ambil direktori proyek (opsional, untuk referensi file lokal)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Koneksi ke MySQL tanpa password
    # Format URI: mysql+pymysql://<user>:<password>@<host>/<database>
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/bulok'
    
    # Matikan notifikasi modifikasi SQLAlchemy (supaya lebih ringan)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key untuk session Flask
    SECRET_KEY = 'bulok-secret-key'


