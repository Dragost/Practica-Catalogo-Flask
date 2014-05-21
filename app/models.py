# -*- coding: utf-8 -*-

from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, DateTime, Integer, String, Text, Boolean, Column, Float
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  username = Column(String)
  pw = Column(String)
  admin = Column(Boolean, default=0)

  def __init__(self, username, passw):
    self.username = username
    self.set_password(passw)

  def set_password(self, passw):
    self.pw = generate_password_hash(passw)

  def check_password(self, pw):
    return check_password_hash(self.pw, pw)

class Product(Base):
  __tablename__ = 'products'
  pid = Column(Integer, primary_key=True)
  name = Column(Text)
  desc = Column(Text)
  stock = Column(Integer)
  price = Column(Float, default=0)