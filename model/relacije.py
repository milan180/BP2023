from sqlalchemy.orm import relationship

from .gosti import Gosti
from .konobari import Konobari
from .narudzbe import Narudzbe
from .pica import Pica
from .stavke_narudzbe import Stavke_narudzbe
from .stolovi import Stolovi

from . import Base
from . import engine


Gosti.narudzbe = relationship("Narudzbe", back_populates="gosti")
Narudzbe.gosti = relationship("Gosti", back_populates="narudzbe")

Konobari.stolovi = relationship("Stolovi", back_populates="konobari")
Stolovi.konobari = relationship("Konobari", back_populates="stolovi")


Stavke_narudzbe.narudzbe = relationship("Narudzbe", back_populates="stavke_narudzbe")
Narudzbe.stavke_narudzbe = relationship("Stavke_narudzbe", back_populates = "narudzbe")

Stavke_narudzbe.pica = relationship("Pica", back_populates="stavke_narudzbe")
Pica.stavke_narudzbe = relationship("Stavke_narudzbe", back_populates="pica")


Base.metadata.bind = engine
Base.metadata.create_all(engine)

