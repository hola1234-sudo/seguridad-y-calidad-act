from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB_FILE = "test.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, stock INTEGER)''')
    
    c.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'admin123')")
    c.execute("INSERT OR IGNORE INTO products (id, name, stock) VALUES (1, 'Laptop', 10)")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return "Bienvenido a la Tienda de Pruebas"

# CP-001: Login con SQL (Aprueba)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')
    
    # Intentionally slightly vulnerable but handles basic injection with a generic error
    if "'" in username or '"' in username:
        return jsonify({"error": "Error de inicio de sesión genérico"}), 400
        
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    
    if user:
        return jsonify({"message": "Login exitoso"}), 200
    return jsonify({"error": "Credenciales inválidas"}), 401

# CP-002: Registro de usuario (Falla, "el botón no responde" -> simulamos error 500)
@app.route('/register', methods=['POST'])
def register():
    # Simulando el error BUG-002 reportado (falla en el registro)
    raise Exception("Error interno: no se puede completar el registro.")
    
# CP-003: Compra de producto (Bloqueado)
@app.route('/buy', methods=['POST'])
def buy():
    # Requiere usuario registrado, pero como el registro falla, no se puede llegar aquí en el flujo normal
    return jsonify({"message": "Producto comprado"}), 200

if __name__ == '__main__':
    if not os.path.exists(DB_FILE):
        init_db()
    app.run(debug=True, port=5000)
