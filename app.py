import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, Cliente
from forms import LoginForm
from flask import request

app = Flask(__name__)
# Clave secreta para proteger los formularios (En producción usa una variable de entorno)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu_clave_secreta_super_segura_123') 
database_url = os.environ.get('DATABASE_URL', 'sqlite:///clientes.db')
# Render a veces envía "postgres://" en lugar de "postgresql://", esto lo arregla:
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Si no está logueado, lo manda aquí

@login_manager.user_loader
def load_user(user_id):
    return Cliente.query.get(int(user_id))

# --- RUTAS ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('portal_cliente'))
        
    form = LoginForm()
    if form.validate_on_submit():
        print(f"🕵️‍♂️ DEBUG: Formulario válido. Usuario ingresado: {form.username.data}")
        user = Cliente.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            print("✅ DEBUG: Contraseña correcta. Iniciando sesión...")
            login_user(user)
            return redirect(url_for('portal_cliente'))
        else:
            print("❌ DEBUG: Usuario no encontrado o contraseña incorrecta.")
            flash('Usuario o contraseña incorrectos', 'error')
    else:
        if request.method == 'POST':
            # Si el formulario falla, imprimimos los errores exactos en la consola
            print(f"🚨 DEBUG: El formulario falló la validación. Errores: {form.errors}")
            flash('Error en el formulario. Revisa los datos.', 'error')
            
    return render_template('login.html', form=form)
@app.route('/portal')
@login_required # Esta es la magia que protege la ruta
def portal_cliente():
    return render_template('portal.html', cliente=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Comando para crear la base de datos la primera vez
@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.create_all()
        print("Base de datos creada.")

if __name__ == '__main__':
    app.run(debug=True)