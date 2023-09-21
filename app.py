from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user  
import re
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration de la base de données SQLite3
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.secret_key = 'fredkesse1234'  # Définissez une clé secrète pour les messages flash
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80))
    prenom = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    mdp = db.Column(db.String(80))

    def __init__(self, nom, prenom, email, mdp):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mdp = mdp


with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Erreur lors de la création de la table : {e}")

@app.route('/')
def index():
    return render_template('index.html')
# tant que l'utilisateur n'est pas connecté, il ne peut pas accéder au dashboard
@app.route('/dashboard')
def dashboard():
    if not session.get('utilisateur'):
        return redirect(url_for('show_login'))
    else:
        return render_template('dashboard.html', user_nom=session.get('utilisateur'))
    


@app.route('/show_login')
def show_login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        mdp = request.form['mdp']

        try:
            utilisateur = User.query.filter_by(email=email).first()
            if utilisateur:
                if check_password_hash(utilisateur.mdp, mdp):
                    session['utilisateur'] = utilisateur.nom
                    flash('Connexion réussie.', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Mot de passe incorrect.', 'error')
                    return redirect(url_for('show_login'))
            else:
                flash("L'utilisateur n'existe pas.", 'error')
                return redirect(url_for('show_login'))
        except Exception as e:
            flash(f"Erreur lors de la connexion : {e}", "error")
            return redirect(url_for('show_login'))

    return render_template('login.html')

@app.route('/show_signup')
def show_signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        mdp = request.form['mdp']

        if not nom or not prenom or not email or not mdp:
            flash('Veuillez remplir tous les champs.', 'error')
            return redirect(url_for('show_signup'))
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Veuillez entrer une adresse email valide.', 'error')
            return redirect(url_for('show_signup'))
        elif len(mdp) < 8 or not re.search("[0-9]", mdp) or not re.search("[A-Z]", mdp):
            flash('Le mot de passe doit contenir au moins 8 caractères, caractères spéciaux et des nombre', 'error')
            return redirect(url_for('show_signup'))
        else:
            try:
                #hash le mot de passe
                mdp = generate_password_hash(mdp)
                utilisateur = User(nom, prenom, email, mdp)
                db.session.add(utilisateur)
                db.session.commit()
                flash('Inscription réussie.', 'success')
                return redirect(url_for('show_login'))
            except Exception as e:
                flash(f"Erreur lors de l'inscription : {e}", "error")
                return redirect(url_for('show_signup'))
            
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('utilisateur', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)