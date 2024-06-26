from sqlalchemy import Column, Integer, String, LargeBinary
from database.database import db

class User(db):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50), nullable=False)
  password = Column(String(26), nullable=False)
  token_id = Column(String(200), nullable=True)

  def __repr__(self):
    return f'<User:[id:{self.id}, name:{self.name}, password:{self.password}, token_id:{self.token_id}]>'
  
  def serialize(self):
    return {
      "id": self.id,
      "name": self.name,
      "password": self.password,
      "token_id": self.token_id
      }
  
class Images(db):
  __tablename__ = 'images'

  id = Column(Integer, primary_key=True, autoincrement=True)
  content = Column(LargeBinary, nullable=False)
  user_id = Column(Integer, nullable=False)

  def __repr__(self):
    return f'<User:[id:{self.id}, content:{self.content}, user_id:{self.user_id}]>'
  
  def serialize(self):
    return {
      "id": self.id,
      "content": self.content,
      "user_id": self.user_id

    }