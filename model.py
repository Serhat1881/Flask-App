import sqlite3

class Melon(object):
    """A wrapper object that corresponds to rows in the melons table."""
    def __init__(self, id, melon_type, common_name, price, imgurl, flesh_color, rind_color, seedless):
        self.id = id
        self.melon_type = melon_type
        self.common_name = common_name
        self.price = price
        self.imgurl = imgurl
        self.flesh_color = flesh_color
        self.rind_color = rind_color
        self.seedless = bool(seedless)

    def price_str(self):
        return "$%.2f"%self.price

    def __repr__(self):
        return "<Melon: %s, %s, %s>"%(self.id, self.common_name, self.price_str())

class Customer(object):
    def __init__(self, id, email, givenname, surname, password, telephone, tos_agree, gender, dob, billto_address1, billto_address2, billto_city, billto_state, billto_postalcode, shipto_address1, shipto_address2, shipto_city, shipto_state, shipto_postalcode, region):
        self.id = id
        self.email = email
        self.givenname = givenname
        self.surname = surname
        self.password = password

    def __repr__(self):
        return self.email

def connect():
    conn = sqlite3.connect("melons.db")
    cursor = conn.cursor()
    return cursor

def get_melons():
    """Query the database for the first 30 melons, wrap each row in a Melon object"""
    cursor = connect()
    query = """SELECT id, melon_type, common_name,
                      price, imgurl,
                      flesh_color, rind_color, seedless
               FROM melons
               WHERE imgurl <> ''
               LIMIT 30;"""

    cursor.execute(query)
    melon_rows = cursor.fetchall()

    melons = []

    for row in melon_rows:
        melon = Melon(row[0], row[1], row[2], row[3], row[4], row[5],
                      row[6], row[7])

        melons.append(melon)

    return melons

def get_melon_by_id(id):
    """Query for a specific melon in the database by the primary key"""
    cursor = connect()
    query = """SELECT id, melon_type, common_name,
                      price, imgurl,
                      flesh_color, rind_color, seedless
               FROM melons
               WHERE id = ?;"""

    cursor.execute(query, (id,))

    row = cursor.fetchone()
    
    if not row:
        return None

    melon = Melon(row[0], row[1], row[2], row[3], row[4], row[5],
                  row[6], row[7])
    
    return melon

def get_customer_by_email(email):
    """Query for a specific customer in the database by the email"""
    cursor = connect()
    query = """SELECT id, email, givenname, surname, password, telephone, tos_agree, gender, dob, billto_address1, billto_address2, billto_city, billto_state, billto_postalcode, shipto_address1, shipto_address2, shipto_city, shipto_state, shipto_postalcode, region
               FROM customers
               WHERE email = ?;"""

    cursor.execute(query, (email,))

    row = cursor.fetchone()
    
    if not row:
        return None

    customer = Customer(row[0], row[1], row[2], row[3], row[4], row[5],
                  row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19])
    
    return customer

def add_customer(email, givenname, surname, password):
    conn = sqlite3.connect("melons.db")
    cursor = conn.cursor()

    # Kullanıcıyı veritabanına ekle
    cursor.execute(
        "INSERT INTO customers (email, givenname, surname, password) VALUES (?, ?, ?, ?)",
        (email, givenname, surname, password)
    )

    # Veritabanı işlemini kaydet
    conn.commit()

    # Veritabanı bağlantısını kapat
    conn.close()
def get_all_users():
    # Veritabanı bağlantısı ve sorgulama işlemleri burada gerçekleştirilir
    # Örnek olarak basit bir kullanıcı listesi döndürüyoruz
    return [
        {"id": 1, "username": "serhat", "role": "admin"},
        {"id": 2, "username": "ali", "role": "user"},
        {"id": 3, "username": "veli", "role": "user"},
        {"id": 4, "username": "serkan", "role": "user"},
        {"id": 5, "username": "halil", "role": "user"},
        {"id": 6, "username": "ali", "role": "user"},
        {"id": 7, "username": "ali", "role": "user"}
    ]



import sqlite3
from flask import Flask, request, render_template, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Güvenlik için kullanılan gizli anahtar

# Veritabanı bağlantısı ve imleci oluştur
conn = sqlite3.connect("melons.db")
cursor = conn.cursor()

# Admin sınıfı
class Admin(object):
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

# Admin tablosunu oluştur
cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    );
""")

# Veritabanı işlemini kaydet
conn.commit()

# Giriş sayfası
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Veritabanından kullanıcıyı sorgula
        cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        
        if user:
            session['logged_in'] = True
            session['user_id'] = user[0]
            flash('Giriş Başarılı', 'success')
            return redirect(url_for('admin_panel'))
        else:
            flash('Kullanıcı adı veya şifre hatalı', 'danger')
    
    return render_template('login.html')

# Admin paneli
@app.route('/admin_panel')
def admin_panel():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    # Admin paneli içeriği burada oluşturulabilir
    return "Admin Panel Content"

# Çıkış yap
@app.route('/logout')
def logout():
    session.clear()
    flash('Çıkış Başarılı', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
def update_user_profile(user_id, email, givenname, surname, new_password):
    """Kullanıcının profil bilgilerini günceller."""
    conn = sqlite3.connect("melons.db")
    cursor = conn.cursor()

    # Eğer yeni şifre belirtilmemişse, eski şifreyi alın
    if not new_password:
        cursor.execute("SELECT password FROM customers WHERE id = ?", (user_id,))
        current_password = cursor.fetchone()[0]
    else:
        current_password = new_password

    # Kullanıcı bilgilerini güncelle
    cursor.execute(
        "UPDATE customers SET email = ?, givenname = ?, surname = ?, password = ? WHERE id = ?",
        (email, givenname, surname, current_password, user_id)
    )

    # Veritabanı işlemini kaydet
    conn.commit()

    # Veritabanı bağlantısını kapat
    conn.close()
    