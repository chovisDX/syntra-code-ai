import os
from flask import Flask, render_template

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Ruta principal de la página web
@app.route('/')
def home():
    # Renderiza la plantilla HTML
    return render_template('index.html')

# Este bloque solo se ejecuta si corres el archivo directamente (en tu PC)
if __name__ == '__main__':
    # Mantenemos debug=True para que sigas viendo cambios en tu PC
    app.run(debug=True)