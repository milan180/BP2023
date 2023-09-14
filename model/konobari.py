from . import Base
from sqlalchemy import *


class Konobari(Base):
    __tablename__ = "konobari"
    id = Column(Integer, primary_key = True)
    ime = Column(String(50))
    prezime = Column(String(50))
    broj_stola = Column(Integer, ForeignKey('stolovi.broj_stola'))
    
    
