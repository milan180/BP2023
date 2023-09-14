from . import Base
from sqlalchemy import *

class Pica(Base):
    __tablename__ = "pica"
    id = Column(Integer, primary_key = True)
    naziv = Column(String(50))
    Opis = Column(Text)
    cijena = Column(Integer)
    kategorija =Column(String(50))
