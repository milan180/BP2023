from . import Base
from sqlalchemy import *

class Stolovi(Base):
    __tablename__ = "stolovi"
    broj_stola = Column(Integer, primary_key = True)
    broj_sjedala = Column(Integer)
    lokacija = Column(String(50))
    status = Column(Boolean)
