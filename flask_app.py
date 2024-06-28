from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# Veritabanı bağlantısını yapılandır
db = mysql.connector.connect(
    host="drmurataltun.mysql.pythonanywhere-services.com",
    user="drmurataltun",
    passwd="alt-239348",
    database="drmurataltun$db_bootcamp"
)

app = Flask(__name__)

# Veritabanında users tablosunu oluştur
def create_users_table():
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)
    db.commit()
    cursor.close()

# Uygulama başladığında users tablosunu oluştur
#create_users_table()

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT name FROM users")  # Kullanıcı isimlerini çek
    user_names = cursor.fetchall()  # Tüm sonuçları bir listeye al
    cursor.close()
    return render_template('index.html', user_names=user_names)  # Sonuçları şablona geçir

@app.route('/signup')
def signup():
    return render_template ('signup2.html')

@app.route('/kayitol', methods=['GET', 'POST'])
def kayitol():
    if request.method == 'POST':
        try:
            # Formdan gelen verileri al
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']

            # Veritabanına kayıt ekle
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            db.commit()
            cursor.close()

            # Kayıttan sonra istediğiniz bir sayfaya yönlendirme
            return redirect(url_for('index'))
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            # Hata durumunda kullanıcıyı bilgilendirecek bir sayfaya yönlendirme yapabilirsiniz
            # return render_template('error.html', error=err)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
