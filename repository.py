import datetime
import os
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, String, Table, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import delete, false, select
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime

db_string = os.environ.get('DB_URL')
base = declarative_base()

class User(base):  
    __tablename__ = 'users'
    id = Column(String, primary_key=True, unique=True)
    name = Column(String)
    alias = Column(String)
    traderItem = Column(Integer)    

    def __init__(self, id, name, alias):
        self.id=id
        self.name = name
        self.alias = alias

class Repository:
    def CommitTransaction(self):
        self.session.commit() 

    def AddUser(self, id, name, alias):
        user = User(id, name, alias)
        self.session.add(user)
        try:
            self.session.commit() 
            return True  
        except:
            return False 

    def DeleteUser(self, id):        
        try:
            user = self.session.get(User, id)
            self.session.delete(user)
            self.session.commit()
            return True
        except:
            return False
    
    def GetUsers(self):        
        try:
            return self.session.query(User).all()
        except:
            return None
    
    def UpdateUser(self, id, traderItem):
        try:
            user: User = self.session.query(User).filter(User.id==id).first()
            user.traderItem = traderItem
            return True
        except:
            return False


    def GetUser(self, id):        
        try:
            return self.session.query(User).filter(User.id==id).first()
        except:
            return None        
        
    def __init__(self):        
        db = create_engine(db_string) 
        base.metadata.create_all(db)
        Session = sessionmaker(db)  
        self.session = Session()

repository = Repository()