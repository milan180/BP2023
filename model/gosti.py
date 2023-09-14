from . import Base
from sqlalchemy import *


class Gosti(Base):
    __tablename__ = "Gosti"
    id = Column(Integer, primary_key = True)
    ime = Column(String(50))
    prezime = Column(String(50))
    broj_stola = Column(Integer)
    status_narudzbe =Column(Boolean)
    
    

    

