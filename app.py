#!/usr/bin/python
#-*- coding: utf-8 -*-
#Autor: Luis Angel Ramirez Mendoza
#______________________________________________________________________________________________________________________
#http://127.0.0.1:5000/geolocalizacion
#http://127.0.0.1:5000/camara

from flask import Flask, Response, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os, folium
import base64
import json
import uuid 
import time
from PIL import Image
from io import BytesIO
import random
import string

app = Flask(__name__)

path = os.getcwd() + "/output/"
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'clave_secreta_segura'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Genera un nombre aleatorio para las imágenes
def generate_random_filename():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.png'

# Usuarios ficticios para hacer login (se podría usar una base de datos)
usuarios_validos = {
    "admin": "admin",
    "usuario2": "admin2024"
}

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def iniciar_sesion():
    usuario = request.form['usuario']
    password = request.form['password']
    
    # Verificar si el usuario y la contraseña coinciden con los datos almacenados
    if usuario in usuarios_validos and usuarios_validos[usuario] == password:
        session['usuario'] = usuario
        return redirect(url_for('principal'))
    else:
        return "Usuario o contraseña incorrectos, intenta de nuevo."

@app.route('/principal')
def principal():
    if 'usuario' in session:
        return render_template('principal.html', usuario=session['usuario'])
    else:
        return redirect(url_for('login'))   


@app.route('/geolocalizacion')
def geo():    
    return render_template('geolocalizacion.html')

@app.route('/geolocalizacion', methods=['POST'])
def recibir_localizacion():
    data = request.get_json()  # Obtener los datos JSON de la solicitud
    latitud = data.get('latitud')
    longitud = data.get('longitud')
    with open("coordenadas.txt", 'w') as fichero:
        fichero.write(str(latitud))
        fichero.write(", ")
        fichero.write(str(longitud))
        fichero.close()        
      
    print(f"Latitud: {latitud}, Longitud: {longitud}")
    return jsonify({"status": "success", "latitud": latitud, "longitud": longitud})

@app.route('/coordenadas')
def coord():
     if 'usuario' in session:
        mapa = folium.Map(location=[20.0, 0.0], zoom_start=2)
        with open('coordenadas.txt', 'r') as file:
            for line in file:
                lat, lon = map(float, line.strip().split(','))
                folium.Marker(location=[lat, lon], popup=f'({lat}, {lon})', icon=folium.Icon(color='blue')).add_to(mapa)
        mapa.save(path + "Location.html")

        with open(path + "Location.html", "r") as f:
            content = f.read()
        return Response(content, mimetype='text/html')

     else:
        return redirect(url_for('login'))

@app.route('/camara')
def cam():
    return render_template('camara.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Obtenemos la imagen desde el cuerpo de la solicitud (en formato base64)
        data_url = request.json['image']
        
        # Eliminar el encabezado de la imagen base64
        header, encoded = data_url.split(",", 1)
        image_data = base64.b64decode(encoded)

        # Cargar la imagen en PIL para guardar el archivo
        image = Image.open(BytesIO(image_data))

        # Generar un nombre de archivo aleatorio
        filename = generate_random_filename()

        # Guardar la imagen en la carpeta designada
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)

        return jsonify({"message": "Image uploaded successfully", "filename": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ver')
def ver():
    if 'usuario' in session:
        image_folder = os.path.join(app.static_folder, 'uploads')
        image_files = os.listdir(image_folder)
        image_files = [img for img in image_files if img.endswith(('png'))]

        return render_template('ver.html', image_files=image_files)

    else:
        return redirect(url_for('login'))

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('usuario', None)  # Elimina la sesión del usuario
    return redirect(url_for('login'))

@app.route('/salir')
def salir():    
    return render_template('salir.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')

