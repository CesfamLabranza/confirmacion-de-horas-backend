from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import requests

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "🟢 Backend activo y listo para procesar PDF"

@app.route("/procesar-pdf", methods=["POST"])
def procesar_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No se envió archivo"}), 400

    file = request.files['file']
    doc = fitz.open(stream=file.read(), filetype="pdf")

    pacientes = []

    for page in doc:
        texto = page.get_text()
        nombre = extraer_valor(texto, "Nombre:")
        fecha = extraer_valor(texto, "Fecha Cita:")
        telefono = extraer_valor(texto, "Teléfono:")

        pacientes.append({
            "nombre": nombre,
            "fecha": fecha,
            "telefono": telefono
        })

        # Enviar a webhook de n8n (ACTUALIZADO CON NGROK)
        requests.post(
            "https://2a4f54982099.ngrok-free.app/webhook-test/recordatorio-citas",
            json=pacientes[-1]
        )

    return jsonify({"estado": "ok", "pacientes": pacientes})

def extraer_valor(texto, campo):
    try:
        inicio = texto.index(campo) + len(campo)
        fin = texto.index("\n", inicio)
        return texto[inicio:fin].strip()
    except:
        return ""
