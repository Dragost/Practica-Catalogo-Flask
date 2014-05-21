# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, flash, session, url_for, redirect, abort
from forms import LoginForm, RegisterForm, AddProductForm, EditProductForm
from models import Base, User, Product
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
from datetime import datetime
from conf import *
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# Configuración App
app = Flask(__name__)
app.config.from_object(__name__)

# Configuración SQL Alchemy
db = SQLAlchemy(app)
db.Model = Base


# Decoradores
def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if 'username' not in session:
      return redirect(url_for('login', next=request.url))
    return f(*args, **kwargs)
  return decorated_function

def logged(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if 'username' in session:
      return redirect(url_for('main', next=request.url))
    return f(*args, **kwargs)
  return decorated_function

# Rutas
@app.route('/', methods=['GET', 'POST'])
def login():
  """Formulario de login"""

  if 'username' in session:
    session['id'] = db.session.query(User).filter_by(username=session['username']).first().id
    return redirect(url_for('main'))

  form = LoginForm(request.form)

  if request.method == 'POST' and form.validate(db):
    session['username'] = form.username.data
    session['id'] = db.session.query(User).filter_by(username=form.username.data).first().id
    session['admin'] = db.session.query(User).filter_by(username=form.username.data).first().admin
    return redirect(url_for('main'))

  return render_template('home.html', form=form)

@app.route('/main/')
@login_required
def main():
  """Lista de Productos"""

  main = {}
  main_a = db.session.query(Product).order_by(Product.name.desc())
  main['products'] = main_a

  return render_template('main.html', main=main)

@app.route('/main/add/', methods=['GET', 'POST'])
@login_required
def addproduct():
  """Añadir Producto"""

  form = AddProductForm(request.form)

  if request.method == 'POST' and form.validate():
    product = Product()
    form.populate_obj(product)
    db.session.add(product)
    db.session.commit()
    return redirect(url_for('main'))

  return render_template('addproduct.html', form=form)

@app.route('/main/delete/<int:pid>/')
@login_required
def delete(pid):
  """Borrar Producto"""

  product = db.session.query(Product).get(pid)

  if product is None :
    abort(404)

  db.session.delete(product)
  db.session.commit()
  return redirect(url_for('main'))

@app.route('/main/edit/<int:pid>/', methods=['GET', 'POST'])
@login_required
def edit(pid):
  """Editar Producto"""

  form = EditProductForm(request.form)

  product = db.session.query(Product).get(pid)

  if product is None :
    abort(404)

  if request.method == 'POST' and form.validate():
    product = db.session.query(Product).get(pid)

    if form.name.data:
      product.name = form.name.data
    if form.desc.data:
      product.desc = form.desc.data
    if form.stock.data:
      product.stock = form.stock.data
    if form.price.data:
      product.price = form.price.data

    db.session.commit()

    return redirect(url_for('main'))

  return render_template('edit.html', product=product, form=form)



@app.route('/users/register/', methods=['GET', 'POST'])
@logged
def register():
  """Formulario de registro"""

  form = RegisterForm(request.form)

  if request.method == 'POST' and form.validate(db):
    newuser = User(form.username.data.lower(), form.password.data)
    db.session.add(newuser)
    db.session.commit()

    session['username'] = newuser.username
    return redirect(url_for('login'))

  return render_template('register.html', form=form)

@app.route('/users/logout/')
@login_required
def logout():
  """Logout"""

  session.pop('username', None)
  session.pop('id', None)
  session.pop('admin', None)
  return redirect(url_for('login'))

@app.route('/users/')
def users():
  """Lista de usuarios"""

  users = db.session.query(User).order_by(User.username.asc())
  return render_template('users.html', users=users)



# Errores
@app.errorhandler(404)
def notfound(e):
  return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(e):
  return render_template('403.html'), 403

# Lanzamos el servidor
if __name__ == '__main__':
  app.run(debug=True)