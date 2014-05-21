# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import Form, TextField, TextAreaField, SubmitField, PasswordField, SelectField, validators
from models import User

class LoginForm(Form):
  username = TextField("Usuario",  [validators.Required("Introduce tu nombre de usuario.")])
  password = PasswordField(u"Contraseña", [validators.Required(u"Introduce la contraseña.")])
  submit = SubmitField("Entrar")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self, db):
    if not Form.validate(self):
      return False

    user = db.session.query(User).filter_by(username = self.username.data.lower()).first()
    if user and user.check_password(self.password.data):
      return True
    elif not user:
      self.username.errors.append("Ese usuario no existe")
      return False
    else:
      self.username.errors.append(u"Usuario y/o contraseña incorrectos")
      return False

class RegisterForm(Form):
  username = TextField("Nombre",  [validators.Required("Introduce tu nombre.")])
  password = PasswordField(u"Contraseña", [validators.Required(u"Introduce una contraseña.")])
  submit = SubmitField("Registrarse")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self, db):
    if not Form.validate(self):
      return False

    user = db.session.query(User).filter_by(username = self.username.data.lower()).first()
    if user:
      self.username.errors.append("Ese nombre de usuario ya esta en uso.")
      return False
    else:
      return True


class AddProductForm(Form):
  name = TextField(u"Nombre", [validators.Required("Introduce Nombre.")])
  desc = TextAreaField(u"Descripción", [validators.Required("Introduce una descripción.")])
  stock = TextField(u"Stock", [validators.Required("Introduce Stock.")])
  price = TextField(u"Precio", [validators.Required("Introduce Precio.")])
  submit = SubmitField("Guardar")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    else:
      return True

class EditProductForm(Form):
  name = TextField(u"Nombre")
  desc = TextAreaField(u"Descripción")
  stock = TextField(u"Stock")
  price = TextField(u"Precio")
  submit = SubmitField("Guardar")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    if not Form.validate(self):
      return False
    else:
      return True