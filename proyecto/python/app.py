from flask import Flask, render_template_string, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import boto3
from decimal import Decimal

app = Flask(__name__)
app.secret_key = 'sellphones-secret-key'

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tabla_usuarios = dynamodb.Table('usuarios')
tabla_celulares = dynamodb.Table('celulares')

style = """
<style>
    body {
        background-color: #fff;
        color: #000;
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .login-container {
        display: flex;
        flex-direction: row;
        gap: 50px;
        justify-content: center;
        margin-top: 100px;
        flex-wrap: wrap;
    }
    .form-box {
        background-color: #f9f9f9;
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 30px;
        width: 300px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    .form-box h2 {
        margin-top: 0;
    }
    .form-box input[type="text"],
    .form-box input[type="password"],
    .form-box input[type="submit"] {
        width: 100%;
        padding: 10px;
        margin-top: 10px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    .form-box input[type="submit"] {
        background-color: #000;
        color: white;
        border: none;
        cursor: pointer;
    }
    .form-box input[type="submit"]:hover {
        background-color: #333;
    }
    .message {
        margin-top: 20px;
        color: green;
        font-weight: bold;
    }
    .container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 20px;
        margin: 30px auto;
        padding: 10px;
    }
    .card {
        background-color: #f0f0f0;
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 20px;
        width: 250px;
        box-sizing: border-box;
        text-align: center;
    }
    .card img {
        width: 100%;
        height: 250px;
        object-fit: cover;
        border-radius: 5px;
    }
    button {
        background-color: #000;
        color: #fff;
        border: none;
        padding: 10px;
        margin-top: 10px;
        cursor: pointer;
        width: 100%;
        border-radius: 5px;
    }
    button:hover {
        background-color: #333;
    }
    table {
        width: 90%;
        margin: auto;
        margin-top: 20px;
        border-collapse: collapse;
    }
    th, td {
        border: 1px solid #ccc;
        padding: 10px;
    }
    th {
        background-color: #ccc;
        color: #000;
    }
</style>
"""

login_html = style + """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <div class="login-container">
        <div class="form-box">
            <h2>Iniciar Sesión</h2>
            <form method="post" action="/login">
                <input type="text" name="username" placeholder="Usuario">
                <input type="password" name="password" placeholder="Contraseña">
                <input type="submit" value="Entrar">
            </form>
        </div>
        <div class="form-box">
            <h2>Registrar</h2>
            <form method="post" action="/register">
                <input type="text" name="username" placeholder="Usuario">
                <input type="password" name="password" placeholder="Contraseña">
                <input type="submit" value="Registrar">
            </form>
            {% if mensaje %}
            <div class="message">{{ mensaje }}</div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

main_page_html = style + """
<!DOCTYPE html>
<html>
<head><title>Sellphones</title></head>
<body>
    <div style="display: flex; justify-content: flex-end; background-color: #f0f0f0; padding: 10px 20px; gap: 10px; align-items: center;">
        <form action="/admin" method="get" style="margin-right: 10px;">
            <button type="submit">Vista Admin</button>
        </form>
        <form action="/logout" method="get">
            <button type="submit">Cerrar sesión</button>
        </form>
    </div>
    <h1>Bienvenido a Sellphones, {{ username }}</h1>
    <div class="container">
        {% for celular in celulares %}
        <div class="card">
            <h3>{{ celular.nombre }}</h3>
            <img src="{{ celular.imagen }}">
            <p>Precio: ${{ celular.precio }}</p>
            <p>Stock: {{ celular.stock }}</p>
            <form method="post" action="/agregar_carrito">
                <input type="hidden" name="nombre" value="{{ celular.nombre }}">
                <input type="hidden" name="precio" value="{{ celular.precio }}">
                <button type="submit">Agregar al carrito</button>
            </form>
        </div>
        {% endfor %}
    </div>
    <h2>Carrito de compras</h2>
    <table>
        <tr><th>Producto</th><th>Precio unitario</th><th>Cantidad</th><th>Subtotal</th><th>Acciones</th></tr>
        {% for item in carrito %}
        <tr>
            <td>{{ item.nombre }}</td>
            <td>${{ item.precio }}</td>
            <td>{{ item.cantidad }}</td>
            <td>${{ item.precio * item.cantidad }}</td>
            <td>
                <form method="post" action="/eliminar_carrito" style="display:inline;">
                    <input type="hidden" name="nombre" value="{{ item.nombre }}">
                    <button type="submit">Eliminar uno</button>
                </form>
            </td>
        </tr>
        {% endfor %}
        <tr>
            <td colspan="3" style="text-align: right;"><strong>Total:</strong></td>
            <td colspan="2"><strong>${{ total }}</strong></td>
        </tr>
    </table>
    {% if carrito %}
    <form method="post" action="/comprar">
        <button type="submit">Comprar ahora</button>
    </form>
    {% endif %}
</body>
</html>
"""

admin_html = style + """
<!DOCTYPE html>
<html>
<head><title>Vista Admin</title></head>
<body>
    <div style="display: flex; justify-content: flex-end; background-color: #f0f0f0; padding: 10px 20px; gap: 10px; align-items: center;">
        <form action="/" method="get" style="margin-right: 10px;">
            <button type="submit">Vista Usuario</button>
        </form>
        <form action="/logout" method="get">
            <button type="submit">Cerrar sesión</button>
        </form>
    </div>

    <h1>Vista de administrador</h1>
    {% if mensaje %}
        <div class="message">{{ mensaje }}</div>
    {% endif %}

    <div class="container">
        {% for celular in celulares %}
        <div class="card">
            <h3>{{ celular.nombre }}</h3>
            <img src="{{ celular.imagen }}">
            <p>Precio: ${{ celular.precio }}</p>
            <p>Stock: {{ celular.stock }}</p>
        </div>
        {% endfor %}
    </div>

    <div class="form-box" style="width: 300px; margin: auto; padding: 20px; background-color: #f9f9f9; border-radius: 10px;">
        <h2>Agregar nuevo celular</h2>
        <form method="post">
            <input type="text" name="nombre" placeholder="Nombre" required><br>
            <input type="text" name="precio" placeholder="Precio" required><br>
            <input type="text" name="imagen" placeholder="URL Imagen" required><br>
            <input type="number" name="stock" placeholder="Stock" required><br>
            <input type="submit" value="Agregar">
        </form>
    </div>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(login_html, mensaje=None)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if not username or not password:
        return render_template_string(login_html, mensaje="Por favor completa todos los campos")

    try:
        response = tabla_usuarios.get_item(Key={'username': username})
        user = response.get('Item')
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['carrito'] = []
            celulares = tabla_celulares.scan().get('Items', [])
            return render_template_string(main_page_html, username=username, celulares=celulares, carrito=session['carrito'])
        else:
            return render_template_string(login_html, mensaje="Credenciales incorrectas")
    except Exception as e:
        return render_template_string(login_html, mensaje=f"Error: {str(e)}")

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    if not username or not password:
        return render_template_string(login_html, mensaje="Por favor completa todos los campos")

    try:
        existing = tabla_usuarios.get_item(Key={'username': username}).get('Item')
        if existing:
            return render_template_string(login_html, mensaje="El usuario ya existe")

        hashed_password = generate_password_hash(password)
        tabla_usuarios.put_item(Item={'username': username, 'password': hashed_password})
        return render_template_string(login_html, mensaje="Usuario registrado correctamente")
    except Exception as e:
        return render_template_string(login_html, mensaje=f"Error: {str(e)}")

@app.route('/agregar_carrito', methods=['POST'])
def agregar_carrito():
    if 'carrito' not in session:
        session['carrito'] = []

    nombre = request.form['nombre']
    precio = Decimal(request.form['precio'])

    try:
        response = tabla_celulares.get_item(Key={'nombre': nombre})
        celular = response.get('Item')
        if not celular:
            mensaje = "Producto no encontrado"
        else:
            stock = int(celular.get('stock', 0))
            carrito = session['carrito']
            for item in carrito:
                if item['nombre'] == nombre:
                    if item['cantidad'] < stock:
                        item['cantidad'] += 1
                        mensaje = None
                    else:
                        mensaje = "No hay más stock disponible"
                    break
            else:
                if stock > 0:
                    carrito.append({'nombre': nombre, 'precio': precio, 'cantidad': 1})
                    mensaje = None
                else:
                    mensaje = "Producto agotado"

            session['carrito'] = carrito
            celulares = tabla_celulares.scan().get('Items', [])
            total = sum(float(item['precio']) * int(item['cantidad']) for item in carrito)
            return render_template_string(main_page_html, username=session['username'], celulares=celulares, carrito=carrito, total=total, mensaje_stock=mensaje)

    except Exception as e:
        mensaje = f"Error al obtener stock: {str(e)}"
        celulares = tabla_celulares.scan().get('Items', [])
        total = sum(item['precio'] * item['cantidad'] for item in session['carrito'])
        return render_template_string(main_page_html, username=session['username'], celulares=celulares, carrito=session['carrito'], total=total, mensaje_stock=mensaje)

@app.route('/eliminar_carrito', methods=['POST'])
def eliminar_carrito():
    nombre = request.form['nombre']
    carrito = session.get('carrito', [])
    for item in carrito:
        if item['nombre'] == nombre:
            item['cantidad'] -= 1
            if item['cantidad'] <= 0:
                carrito.remove(item)
            break
    session['carrito'] = carrito
    celulares = tabla_celulares.scan().get('Items', [])
    total = sum(float(item['precio']) * int(item['cantidad']) for item in carrito)
    return render_template_string(main_page_html, username=session['username'], celulares=celulares, carrito=carrito, total=total)

@app.route('/comprar', methods=['POST'])
def comprar():
    carrito = session.get('carrito', [])
    if not carrito:
        return "<h3 style='color:red;'>El carrito está vacío</h3><a href='/'>Volver</a>"

    try:
        for item in carrito:
            nombre = item['nombre']
            cantidad = item['cantidad']

            response = tabla_celulares.get_item(Key={'nombre': nombre})
            celular = response.get('Item')
            if not celular:
                return f"<h3 style='color:red;'>Producto {nombre} no encontrado</h3><a href='/'>Volver</a>"
            stock = int(celular.get('stock', 0))

            if stock < cantidad:
                return f"<h3 style='color:red;'>Stock insuficiente para {nombre}</h3><a href='/'>Volver</a>"

            nuevo_stock = stock - cantidad
            tabla_celulares.update_item(
                Key={'nombre': nombre},
                UpdateExpression='SET stock = :val',
                ExpressionAttributeValues={':val': nuevo_stock}
            )

        session['carrito'] = []
        celulares = tabla_celulares.scan().get('Items', [])
        return render_template_string(main_page_html, username=session['username'], celulares=celulares, carrito=[])
    except Exception as e:
        return f"<h3 style='color:red;'>Error al procesar la compra: {str(e)}</h3><a href='/'>Volver</a>"

@app.route('/admin', methods=['GET', 'POST'])
def vista_admin():
    if 'username' not in session:
        return redirect('/')

    mensaje = None

    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            precio = Decimal(request.form['precio'])
            imagen = request.form['imagen']
            stock = int(request.form['stock'])

            if not nombre or not imagen:
                mensaje = "Todos los campos son obligatorios"
            else:
                tabla_celulares.put_item(Item={
                    'nombre': nombre,
                    'precio': precio,
                    'imagen': imagen,
                    'stock': stock
                })
                mensaje = "Celular agregado exitosamente"
        except Exception as e:
            mensaje = f"Error: {str(e)}"

    celulares = tabla_celulares.scan().get('Items', [])
    return render_template_string(admin_html, username=session['username'], celulares=celulares, mensaje=mensaje)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
