from flask import Flask, render_template_string, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import boto3
from uuid import uuid4

app = Flask(__name__)
app.secret_key = 'sellphones-secret-key'

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tabla_usuarios = dynamodb.Table('usuarios')
tabla_celulares = dynamodb.Table('celulares')

# Estilos
style = """
<style>
    body {
        background-color: #000;
        color: #0f0;
        font-family: Arial, sans-serif;
        text-align: center;
    }
    .container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
        margin-top: 30px;
    }
    .card {
        background-color: #111;
        border: 1px solid #0f0;
        border-radius: 10px;
        padding: 20px;
        width: 250px;
    }
    img {
        width: 100%;
        height: auto;
        border-radius: 5px;
    }
    button {
        background-color: #0f0;
        color: #000;
        border: none;
        padding: 10px;
        margin-top: 10px;
        cursor: pointer;
        width: 100%;
        border-radius: 5px;
    }
    table {
        width: 80%;
        margin: auto;
        margin-top: 20px;
        border-collapse: collapse;
    }
    th, td {
        border: 1px solid #0f0;
        padding: 10px;
    }
    th {
        background-color: #0f0;
        color: #000;
    }
</style>
"""

login_html = style + """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <h2>Iniciar Sesión</h2>
    <form method="post" action="/login">
        Usuario: <input type="text" name="username"><br>
        Contraseña: <input type="password" name="password"><br>
        <input type="submit" value="Entrar">
    </form>
    <br>
    <h2>Registrar</h2>
    <form method="post" action="/register">
        Usuario: <input type="text" name="username"><br>
        Contraseña: <input type="password" name="password"><br>
        <input type="submit" value="Registrar">
    </form>
</body>
</html>
"""

main_page_html = style + """
<!DOCTYPE html>
<html>
<head><title>Sellphones</title></head>
<body>
    <h1>Bienvenido a Sellphones, {{ username }}</h1>
    <form action="/logout" method="get">
        <button type="submit">Cerrar sesión</button>
    </form>
    <div class="container">
        {% for celular in celulares %}
        <div class="card">
            <h3>{{ celular.nombre }}</h3>
            <img src="{{ celular.imagen }}">
            <p>Precio: ${{ celular.precio }}</p>
            <form method="post" action="/agregar_carrito">
                <input type="hidden" name="nombre" value="{{ celular.nombre }}">
                <input type="hidden" name="precio" value="{{ celular.precio }}">
                <button type="submit">Comprar</button>
            </form>
        </div>
        {% endfor %}
    </div>
    <h2>Carrito de compras</h2>
    <table>
        <tr><th>Producto</th><th>Precio</th><th>Cantidad</th></tr>
        {% for item in carrito %}
        <tr>
            <td>{{ item.nombre }}</td>
            <td>${{ item.precio }}</td>
            <td>{{ item.cantidad }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(login_html)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if not username or not password:
        return "<h3 style='color:red;'>Por favor completa todos los campos</h3><a href='/'>Volver</a>"

    try:
        response = tabla_usuarios.get_item(Key={'username': username})
        user = response.get('Item')
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['carrito'] = []
            celulares = tabla_celulares.scan().get('Items', [])
            return render_template_string(main_page_html, username=username, celulares=celulares, carrito=session['carrito'])
        else:
            return "<h3 style='color:red;'>Credenciales incorrectas</h3><a href='/'>Volver</a>"
    except Exception as e:
        return f"<h3 style='color:red;'>Error: {str(e)}</h3><a href='/'>Volver</a>"

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    if not username or not password:
        return "<h3 style='color:red;'>Por favor completa todos los campos</h3><a href='/'>Volver</a>"

    try:
        existing = tabla_usuarios.get_item(Key={'username': username}).get('Item')
        if existing:
            return "<h3 style='color:red;'>El usuario ya existe</h3><a href='/'>Volver</a>"

        hashed_password = generate_password_hash(password)
        tabla_usuarios.put_item(Item={'username': username, 'password': hashed_password})
        return "<h3>Usuario registrado correctamente</h3><a href='/'>Volver al login</a>"
    except Exception as e:
        return f"<h3 style='color:red;'>Error: {str(e)}</h3><a href='/'>Volver</a>"

@app.route('/agregar_carrito', methods=['POST'])
def agregar_carrito():
    if 'carrito' not in session:
        session['carrito'] = []

    nombre = request.form['nombre']
    precio = float(request.form['precio'])

    carrito = session['carrito']
    for item in carrito:
        if item['nombre'] == nombre:
            item['cantidad'] += 1
            break
    else:
        carrito.append({'nombre': nombre, 'precio': precio, 'cantidad': 1})

    session['carrito'] = carrito
    celulares = tabla_celulares.scan().get('Items', [])
    return render_template_string(main_page_html, username=session['username'], celulares=celulares, carrito=carrito)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
