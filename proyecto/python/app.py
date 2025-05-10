from flask import Flask, render_template_string, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import boto3

app = Flask(__name__)
app.secret_key = 'sellphones-secret-key'

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tabla_usuarios = dynamodb.Table('usuarios')
tabla_celulares = dynamodb.Table('celulares')

# Estilos actualizados (blanco y negro)
style = """
<style>
    body {
        background-color: #000;
        color: #fff;
        font-family: Arial, sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        flex-direction: column;
        margin: 0;
    }
    .form-box {
        background-color: #111;
        border: 1px solid #fff;
        border-radius: 10px;
        padding: 30px;
        width: 300px;
        text-align: left;
    }
    .form-box h2 {
        text-align: center;
    }
    input[type="text"], input[type="password"] {
        width: 100%;
        padding: 8px;
        margin: 5px 0;
        border: none;
        border-radius: 4px;
    }
    button, input[type="submit"] {
        background-color: #fff;
        color: #000;
        border: none;
        padding: 10px;
        width: 100%;
        margin-top: 10px;
        cursor: pointer;
        border-radius: 5px;
    }
    .container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
        margin-top: 20px;
    }
    .card {
        background-color: #111;
        border: 1px solid #fff;
        border-radius: 10px;
        padding: 20px;
        width: 250px;
    }
    img {
        width: 100%;
        height: auto;
        border-radius: 5px;
    }
    table {
        width: 80%;
        margin: auto;
        margin-top: 20px;
        border-collapse: collapse;
    }
    th, td {
        border: 1px solid #fff;
        padding: 10px;
    }
    th {
        background-color: #fff;
        color: #000;
    }
</style>
"""

# HTML login + register
login_html = style + """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <div class="form-box">
        <h2>Iniciar Sesión</h2>
        <form method="post" action="/login">
            Usuario: <input type="text" name="username" required><br>
            Contraseña: <input type="password" name="password" required><br>
            <input type="submit" value="Entrar">
        </form>
        <br>
        <h2>Registrar</h2>
        <form method="post" action="/register">
            Usuario: <input type="text" name="username" required><br>
            Contraseña: <input type="password" name="password" required><br>
            <input type="submit" value="Registrar">
        </form>
    </div>
</body>
</html>
"""

# Página principal
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
            <p>Stock: {{ celular.stock }}</p>
            {% if celular.stock > 0 %}
            <form method="post" action="/agregar_carrito">
                <input type="hidden" name="nombre" value="{{ celular.nombre }}">
                <input type="hidden" name="precio" value="{{ celular.precio }}">
                <button type="submit">Agregar al carrito</button>
            </form>
            {% else %}
            <p style="color: red;">Agotado</p>
            {% endif %}
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
    {% if carrito %}
    <form method="post" action="/comprar">
        <button type="submit">Comprar ahora</button>
    </form>
    {% endif %}
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

    response = tabla_usuarios.get_item(Key={'username': username})
    user = response.get('Item')
    if user and check_password_hash(user['password'], password):
        session['username'] = username
        session['carrito'] = []
        celulares = tabla_celulares.scan().get('Items', [])
        return render_template_string(main_page_html, username=username, celulares=celulares, carrito=[])
    else:
        return "<h3 style='color:red;'>Credenciales incorrectas</h3><a href='/'>Volver</a>"

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    if not username or not password:
        return "<h3 style='color:red;'>Por favor completa todos los campos</h3><a href='/'>Volver</a>"

    existing = tabla_usuarios.get_item(Key={'username': username}).get('Item')
    if existing:
        return "<h3 style='color:red;'>El usuario ya existe</h3><a href='/'>Volver</a>"

    hashed_password = generate_password_hash(password)
    tabla_usuarios.put_item(Item={'username': username, 'password': hashed_password})
    return "<h3>Usuario registrado correctamente</h3><a href='/'>Volver al login</a>"

@app.route('/agregar_carrito', methods=['POST'])
def agregar_carrito():
    nombre = request.form['nombre']
    precio = float(request.form['precio'])

    if 'carrito' not in session:
        session['carrito'] = []

    for item in session['carrito']:
        if item['nombre'] == nombre:
            item['cantidad'] += 1
            break
    else:
        session['carrito'].append({'nombre': nombre, 'precio': precio, 'cantidad': 1})

    celulares = tabla_celulares.scan().get('Items', [])
    return render_template_string(main_page_html, username=session['username'], celulares=celulares, carrito=session['carrito'])

@app.route('/comprar', methods=['POST'])
def comprar():
    carrito = session.get('carrito', [])
    errores = []

    for item in carrito:
        nombre = item['nombre']
        cantidad = item['cantidad']

        celular = tabla_celulares.get_item(Key={'nombre': nombre}).get('Item')
        if celular and celular['stock'] >= cantidad:
            nuevo_stock = celular['stock'] - cantidad
            tabla_celulares.update_item(
                Key={'nombre': nombre},
                UpdateExpression="SET stock = :s",
                ExpressionAttributeValues={':s': nuevo_stock}
            )
        else:
            errores.append(nombre)

    session['carrito'] = []
    celulares = tabla_celulares.scan().get('Items', [])
    mensaje = "¡Compra realizada con éxito!" if not errores else f"Fallo en: {', '.join(errores)}"
    return render_template_string(main_page_html + f"<p>{mensaje}</p>", username=session['username'], celulares=celulares, carrito=[])

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
