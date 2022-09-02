from flask import Flask, render_template, url_for, request, redirect
from config import *
from notas import Notas

con_db = conection()

app = Flask(__name__)

# ruta de la pagina principal
@app.route("/")
def index():
    return render_template("index.html")

# guardar los usuarios
@app.route("/guardar_notas", methods=['POST'])
def notas_http():
    notass = con_db['notas']  # crea la coleccion con las notas
    nombre = request.form['name']
    nota1 = request.form['nota1']
    nota2 = request.form['nota2']
    nota3 = request.form['nota3']
    print(nombre, nota1, nota2, nota3)
    print(type(nota1))
    if nombre != '' and nota1 != '' and nota2 != '' and nota3 != '':
        nota1 = float(nota1)
        nota2 = float(nota2)
        nota3 = float(nota3)
        notass = con_db['notas']  # crea la coleccion con las notas
        promedioo = promedio(nota1, nota2, nota3)
        criteriob = criterio(promedioo)
        result = Notas(nombre, promedioo, criteriob)
        notass.insert_one(result.formato_doc()) #inserta los datos en la coleccion usuarios
        return render_template("index.html")
    else:
        return render_template("404.html")

# español, matematicas, ingles
# ruta con parametros
#http://localhost:9999/notas/andres espitia/4.4/4.4/4.4
@app.route("/notas/<nombre>/<float:nota1>/<float:nota2>/<float:nota3>")
def notas_ruta(nombre, nota1, nota2, nota3):
    info = {
		'nombre': nombre,
        'nota1': nota1,
        'nota2': nota2,
        'nota3': nota3
	}
    if nombre != '' and nota1 != '' and nota2 != '' and nota3 != '':
        notass = con_db['notas'] #crea la coleccion con las notas
        nota1 = float(nota1)
        nota2 = float(nota2)
        nota3 = float(nota3)
        promedioo = promedio(nota1, nota2, nota3)
        criteriob = criterio(promedioo)
        result = Notas(nombre, promedioo, criteriob)
        notass.insert_one(result.formato_doc()) #inserta los datos en la coleccion usuarios
        return render_template("index.html")
    else:
        return render_template("404.html")

#promedio de las tres notas
def promedio(nota1, nota2, nota3):
    return (nota1 + nota2 + nota3) / 3

#criterio segun la nota
def criterio(promedio):
    if promedio < 1 and promedio > 0:
        return 'Estudiante Reprobado'
    elif promedio >= 1 and promedio < 2.5:
        return 'Estudiante en condicionamiento'
    elif promedio >= 2.5 and promedio < 3:
        return 'Estudiante con probabilidades de aprobar'
    elif promedio >= 3 and promedio < 4:
        return 'Estudiante aprobado'
    elif promedio >= 4 and promedio <= 5:
        return 'Estudiante aprobado con excelente promedio'
    else :
        return 'Nota no valida'

# ruta de error 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == "__main__":
	app.run(debug=True, port=9999)
