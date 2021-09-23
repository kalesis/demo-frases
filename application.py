from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


application = app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# call DB var
db = SQLAlchemy(app)


class Frase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    autor = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():
    # listar frases
    _list = Frase.query.all()
    
    return render_template('index.html', frases=_list)

@app.route("/add", methods=["POST"])
def add():
    """Agregar un NUEVO registro
    """
    title = request.form.get("title")
    autor = request.form.get("autor")
    new = Frase(title=title, autor=autor, complete=False)
    db.session.add(new)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:frase_id>")
def delete(frase_id):
    """DELETE registro
    """
    frase = Frase.query.filter_by(id=frase_id).first()
    db.session.delete(frase)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/about')
def about():
    return "Acerca de nosotros"

@app.route('/newdemo')
def newdemo():
    new = Frase(title='Frase Celebre 1', autor='Anonimo', complete=True)
    db.session.add(new)
    db.session.commit()
    return 'New'

if __name__ == '__main__':
    # crear la BD
    db.create_all()
    # run app
    app.run(debug=True, port=3000)