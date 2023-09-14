from . import Base
from sqlalchemy import *


class Stavke_narudzbe(Base):
    __tablename__ = "stavke_narudzbe"
    id = Column(Integer, primary_key = True)
    ID_narudzba = Column(Integer, ForeignKey('narudzbe.id'))
   
    ID_pica = Column(Integer, ForeignKey('pica.id'))
    
    kolicina = Column(Integer)

