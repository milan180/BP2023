from . import Base
from sqlalchemy import *



class Narudzbe(Base):
    __tablename__ = "narudzbe"
    id = Column(Integer, primary_key = True)
    ID_gosta = Column(Integer, ForeignKey('Gosti.id'))
    
    vrijeme_narudzbe = Column(DateTime)
    status = Column(String(50))
    ukupna_cijena =Column(Integer)

