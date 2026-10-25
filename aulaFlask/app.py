from flask import Flask, redirect, render_template, request, url_for
from markupsafe import escape

app = Flask(__name__)

tareas = [
    {"titulo": "Repasar las funciones", "prioridad": "normal"},
    {"titulo": "Entregar la práctica", "prioridad": "alta"},
]


@app.route("/")
def inicio():
    return render_template("index.html", tareas=tareas)


@app.route("/informacion")
def informacion():
    return "<p>Este tablón organiza las tareas del curso.</p>"


@app.route("/saludo/<nombre>")
def saludo(nombre):
    return f"<h1>Hola, {escape(nombre)}</h1>"


@app.route("/sesion/<int:minutos>")
def sesion(minutos):
    horas = minutos / 60
    return f"<p>{minutos} minutos equivalen a {horas} horas.</p>"


@app.route("/consulta")
def consulta():
    tema = request.args.get("tema", "Flask").strip()
    return f"<p>Consulta recibida: {escape(tema)}</p>"


@app.route("/nueva", methods=["GET", "POST"])
def nueva():
    titulo = ""
    prioridad = "normal"
    error = ""
    estado = 200

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        prioridad = request.form.get("prioridad", "normal")

        if len(titulo) < 3:
            error = "Escribe un título de al menos 3 caracteres."
        elif len(titulo) > 80:
            error = "El título no puede superar los 80 caracteres."
        elif prioridad not in ["normal", "alta"]:
            error = "Selecciona una prioridad válida."
        else:
            tareas.append({"titulo": titulo, "prioridad": prioridad})
            return redirect(url_for("inicio"), code=303)

        estado = 400

    return render_template(
        "nueva.html",
        titulo=titulo,
        prioridad=prioridad,
        error=error,
    ), estado
