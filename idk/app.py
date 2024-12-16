from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

# Inicializace Flask aplikace
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tajny_klic'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tabulka.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializace databáze
db = SQLAlchemy(app)

# Definice modelu pro databázi
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"

# Definice formuláře pomocí WTForms
class UserForm(FlaskForm):
    name = StringField('Jméno', validators=[DataRequired(), Length(min=2, max=100)])
    age = IntegerField('Věk', validators=[DataRequired(), NumberRange(min=1, max=120)])
    submit = SubmitField('Odeslat')

# Route pro základní stránku
@app.route('/')
def index():
    return redirect(url_for('list_users'))

# Route pro zobrazení formuláře a uložení dat do databáze
@app.route('/new', methods=['GET', 'POST'])
def new_user():
    form = UserForm()
    if form.validate_on_submit():
        new_user = User(name=form.name.data, age=form.age.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('list_users'))  
    else:
        print("Formulář nebyl validní:", form.errors)

    return render_template('new_user.html', form=form)

# Route pro zobrazení seznamu uživatelů
@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('list_users.html', users=users)

# Route pro odstranění uživatele
@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('list_users'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Vytvoří tabulky v databázi, pokud ještě neexistují
    # Spuštění aplikace s debug=False kvůli problémům s multiprocessing
    app.run(debug=False)