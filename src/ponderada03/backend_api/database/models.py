from sqlalchemy import Column, Integer, String
from database.database import db

class User(db):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50), nullable=False)
  password = Column(String(26), nullable=False)
  token_id = Column(String(200), nullable=True)

  def __repr__(self):
    return f'<User:[id:{self.id}, name:{self.name}, password:{self.password}]>'
  
  def serialize(self):
    return {
      "id": self.id,
      "name": self.name,
      "password": self.password}