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
    traderItem = Column(String, default="02") 
    session=Column(String)
    api_id=Column(Integer)   
    api_hash=Column(String)
    cws_id=Column(Integer)

    def __init__(self, id, alias, session, api_id, api_hash, cws_id):
        self.id=id
        self.alias = alias
        self.session = session
        self.api_id = api_id
        self.api_hash = api_hash
        self.cws_id = cws_id

class Repository:
    def CommitTransaction(self):
        self.session.commit() 

    def AddUser(self, id, alias, session, api_id, api_hash, cws_id):
        user = User(id, alias, session, api_id, api_hash, cws_id)
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