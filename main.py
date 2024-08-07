import psycopg2
from psycopg2.extras import RealDictCursor
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, render_template, url_for, request, session, flash
from flask_bootstrap import Bootstrap
import db

app = Flask(__name__, template_folder='templates')
bootstrap = Bootstrap(app)

@app.route('/base')
def base():
    return render_template('base.html')

app.secret_key = "vyacorporation"
@app.route('/')
def index():
    if 'tipo_usuario' not in session or session['tipo_usuario'] != 'admin':
        flash('Acceso denegado. Debes ser administrador para acceder a esta página.')
        return redirect(url_for('login'))
    return render_template('login.html')

import psycopg2
from psycopg2.extras import RealDictCursor

@app.route('/acceso-login', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'txtcorreo' in request.form and 'txtPassword' in request.form:
        _correo = request.form['txtcorreo']
        _password = request.form['txtPassword']

        conn = None
        cursor = None
        cuenta = None

        try:
            conn = db.conectar()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute('''
                SELECT * FROM usuarios WHERE correo = %s AND password = %s
            ''', (_correo, _password))
            cuenta = cursor.fetchone()

        except Exception as e:
            print(f"Error: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                db.desconectar(conn)

        if cuenta:
            if cuenta['tipo_usuario'] == 'admin':
                session['tipo_usuario'] = 'admin'
                return redirect(url_for('base'))
            elif cuenta['tipo_usuario'] == 'almacenista':
                session['tipo_usuario'] = 'almacenista'
                return redirect(url_for('almacenista_dashboard'))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html')



@app.route('/admin')
def admin():
    if session.get('logueado'):
        return render_template('admin.html')
    else:
        return render_template('login.html', mensaje="Acceso no autorizado")

# productos
@app.route('/productos')
def productos():
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM Productos_view''')
    datos = cursor.fetchall()
    cursor.close()
    db.desconectar(conn)
    return render_template('productos.html', datos=datos)

@app.route('/delete_productos/<int:id>', methods=['POST'])
def delete_productos(id):
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM Productos_view WHERE id=%s''', (id,))
    conn.commit()
    cursor.close()
    db.desconectar(conn)
    return redirect(url_for('productos'))

@app.route('/update1_productos/<int:id>', methods=['POST'])
def update1_productos(id):
    conn = db.conectar()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Productos_view WHERE id = %s', (id,))
    datos = cursor.fetchall()
    cursor.close()
    db.desconectar(conn)
    return render_template('editar_producto.html', datos=datos)


@app.route('/update2_productos/<int:id>', methods=['POST'])
def update2_productos(id):
    producto = request.form.get('producto')
    cantidad = request.form.get('cantidad')
    categoria = request.form.get('categoria')
    proveedores = request.form.get('proveedores')
    marca = request.form.get('marca')
    bodega = request.form.get('bodega')

    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''UPDATE Productos_view SET producto=%s, cantidad=%s, categoria=%s, proveedores=%s, marca=%s, bodega=%s WHERE id=%s''',
                   (producto, cantidad, categoria, proveedores, marca, bodega, id))
    conn.commit()
    cursor.close()
    db.desconectar(conn)

    return redirect(url_for('productos'))

@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        producto = request.form.get('producto')
        cantidad = request.form.get('cantidad')
        categoria = request.form.get('categoria')
        proveedores = request.form.get('proveedores')
        marca = request.form.get('marca')
        bodega = request.form.get('bodega')

        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute('''
                INSERT INTO productos (producto, cantidad, categoria, proveedores, marca, bodega)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (producto, cantidad, categoria, proveedores, marca, bodega))
        conn.commit()
        cursor.close()
        db.desconectar(conn)

        return redirect(url_for('productos'))

    return render_template('agregar_producto.html')

# bodega
@app.route('/bodega')
def bodega():
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM bodega''')
    datos = cursor.fetchall()
    cursor.close()
    db.desconectar(conn)
    return render_template('Bodega.html', datos=datos)

@app.route('/delete_bodega/<int:id_bodega>', methods=['POST'])
def delete_bodega(id_bodega):
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM bodega WHERE id_bodega=%s''', (id_bodega,))
    conn.commit()
    cursor.close()
    db.desconectar(conn)
    return redirect(url_for('bodega'))

@app.route('/update1_bodega/<int:id_bodega>', methods=['POST'])
def update1_bodega(id_bodega):
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM bodega WHERE id_bodega=%s''', (id_bodega,))
    datos = cursor.fetchall()
    cursor.close()
    db.desconectar(conn)
    return render_template('editar_bodega.html', datos=datos)

@app.route('/update2_bodega/<int:id_bodega>', methods=['POST'])
def update2_bodega(id_bodega):
    bodega = request.form.get('bodega')
    ubicacion = request.form.get('ubicacion')

    conn = db.conectar()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE bodega
        SET bodega = %s,
            ubicacion = %s
        WHERE id_bodega = %s
        ''', (bodega, ubicacion, id_bodega))

    conn.commit()
    cursor.close()
    db.desconectar(conn)

    return redirect(url_for('bodega'))

# usuarios
@app.route('/usuarios')
def usuarios():
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM usuarios ORDER BY id_rol''')
    datos = cursor.fetchall()
    cursor.close()
    db.desconectar(conn)
    return render_template('Usuarios.html', datos=datos)

@app.route('/delete_usuario/<int:id_rol>', methods=['POST'])
def delete_usuario(id_rol):
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM usuarios WHERE id_rol=%s''', (id_rol,))
    conn.commit()
    cursor.close()
    db.desconectar(conn)
    return redirect(url_for('usuarios'))

@app.route('/update1_usuario/<int:id_rol>', methods=['POST'])
def update1_usuario(id_rol):
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM usuarios WHERE id_rol=%s''', (id_rol,))
    datos = cursor.fetchall()
    cursor.close()
    db.desconectar(conn)
    return render_template('editar_usuario.html', datos=datos)

@app.route('/agregar_usuario', methods=['GET', 'POST'])
def agregar_usuario():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido_paterno = request.form.get('apellido_paterno')
        apellido_materno = request.form.get('apellido_materno')
        rol = request.form.get('rol')
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')

        conn = db.conectar()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO usuarios (nombre_usuario, apaterno, amaterno, tipo_usuario, correo, password)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''', (nombre, apellido_paterno, apellido_materno, rol, correo, contraseña))

        conn.commit()
        cursor.close()
        db.desconectar(conn)

        return redirect(url_for('usuarios'))

    return render_template('agregar_usuario.html')


@app.route('/update2_usuario/<int:id_rol>', methods=['POST'])
def update2_usuario(id_rol):
    nombre = request.form.get('nombre')
    apellido_paterno = request.form.get('apellido_paterno')
    apellido_materno = request.form.get('apellido_materno')
    rol = request.form.get('rol')
    correo = request.form.get('correo')
    contraseña = request.form.get('contraseña')

    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE usuarios
        SET nombre_usuario = %s,
            apaterno = %s,
            amaterno = %s,
            tipo_usuario = %s,
            correo = %s,
            password = %s
        WHERE id_rol = %s
        ''', (nombre, apellido_paterno, apellido_materno, rol, correo, contraseña, id_rol))

    conn.commit()
    cursor.close()
    db.desconectar(conn)

    return redirect(url_for('usuarios'))

# proveedores
@app.route('/proveedores')
def proveedores():
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM proveedores''')
    datos = cursor.fetchall()
    cursor.close()
    db.desconectar(conn)
    return render_template('Proveedores.html', datos=datos)

@app.route('/delete_provedores/<int:id_proveedor>', methods=['POST'])
def delete_proveedores(id_proveedor):
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM proveedores WHERE id_proveedor=%s''', (id_proveedor,))
    conn.commit()
    cursor.close()
    db.desconectar(conn)
    return redirect(url_for('proveedores'))

@app.route('/update1_proveedores/<int:id_proveedor>', methods=['POST'])
def update1_proveedores(id_proveedor):
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM proveedores WHERE id_proveedor=%s''', (id_proveedor,))
    datos = cursor.fetchall()
    cursor.close()
    db.desconectar(conn)
    return render_template('editar_proveedor.html', datos=datos)

@app.route('/update2_proveedores/<int:id_proveedor>', methods=['POST'])
def update2_proveedores(id_proveedor):
    proveedores = request.form.get('proveedores')
    telefono = request.form.get('telefono')
    empresa = request.form.get('empresa')

    conn = db.conectar()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE proveedores
        SET proveedores = %s,
            telefono = %s,
            empresa = %s
        WHERE id_proveedor = %s
        ''', (proveedores, telefono, empresa, id_proveedor))

    conn.commit()
    cursor.close()
    db.desconectar(conn)

    return redirect(url_for('proveedores'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
