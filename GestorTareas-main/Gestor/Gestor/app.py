from flask import Flask, render_template, redirect, url_for, request, flash, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'secreto'

client = MongoClient("mongodb://localhost:27017/")
db = client["gestor_tareas"]
usuarios_collection = db["usuarios"]

@app.route('/')
def registro():
    return render_template('registro.html', active_page='registro')

@app.route('/registrar', methods=['POST'])
def registrar():
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    email = request.form['email']
    password = request.form['password']

    if usuarios_collection.find_one({"email": email}):
        flash("Ese correo ya está registrado")
        return redirect(url_for('registro'))

    usuarios_collection.insert_one({
        "nombre": nombre,
        "apellidos": apellidos,
        "email": email,
        "password": password
    })

    flash("Usuario registrado correctamente")
    return redirect(url_for('inicio'))

@app.route('/inicio')
def inicio():
    return render_template('inicio.html', active_page='inicio')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    usuario = usuarios_collection.find_one({
        "email": email,
        "password": password
    })

    if usuario:
        session['usuario'] = email
        flash("Bienvenido")
        return redirect(url_for('tareas'))
    else:
        flash("Correo o contraseña incorrectos")
        return redirect(url_for('inicio'))

@app.route('/tareas')
def tareas():
    if 'usuario' not in session:
        flash("Debes iniciar sesión primero")
        return redirect(url_for('inicio'))

    return render_template('tareas.html', active_page='tareas')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Sesión cerrada")
    return redirect(url_for('registro'))

if __name__ == '__main__':
    app.run(debug=True)