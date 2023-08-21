from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Modèle Client
class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    nom = Column(String(100),unique=True)
    adresse = Column(String(200))
    
    bons_reception = relationship('BonReceptionMatierePremiere', back_populates='client')

    def __str__(self):
        return f"{self.nom}"

# Modèle Matière Première
class MatierePremiere(Base):
    __tablename__ = 'matieres_premieres'

    id = Column(Integer, primary_key=True)
    nom = Column(String(100))
    description = Column(String)
    quantite_stock = Column(Float)
    unite_mesure = Column(String(50))
    date_expiration = Column(Date)
    
    bon_reception_id = Column(Integer, ForeignKey('bons_reception_matieres_premieres.id'))
    
    bon_reception = relationship('BonReceptionMatierePremiere', back_populates='matieres_premieres_recues')


    def __str__(self):
        return self.nom
    
# Modèle Bon de Réception des Matières Premières
class BonReceptionMatierePremiere(Base):
    __tablename__ = 'bons_reception_matieres_premieres'

    id = Column(Integer, primary_key=True)
    date_reception = Column(Date)
    client_id = Column(Integer, ForeignKey('clients.id'))

    client = relationship('Client', back_populates='bons_reception')
    matieres_premieres_recues = relationship('MatierePremiere', back_populates='bon_reception')

# Modèle Produit Fini
class ProduitFini(Base):
    __tablename__ = 'produits_finis'

    id = Column(Integer, primary_key=True)
    nom = Column(String(100))
    description = Column(String)
    prix_vente = Column(Float)
    unite_mesure = Column(String(50))

    def __str__(self):
        return self.nom

# Modèle Facture
class Facture(Base):
    __tablename__ = 'factures'

    id = Column(Integer, primary_key=True)
    numero_facture = Column(String(20))
    date_facturation = Column(Date)
    montant_total = Column(Float)
    client_id = Column(Integer, ForeignKey('clients.id'))

    client = relationship('Client')
    produits_vendus = relationship('ProduitFini', secondary='facture_produit_fini')

# Table d'association Facture-ProduitFini
facture_produit_fini = Table('facture_produit_fini', Base.metadata,
    Column('facture_id', Integer, ForeignKey('factures.id')),
    Column('produit_fini_id', Integer, ForeignKey('produits_finis.id'))
)





# Modèle Ordre de Production
class OrdreProduction(Base):
    __tablename__ = 'ordres_production'

    id = Column(Integer, primary_key=True)
    date_creation = Column(Date)
    produit_fini_id = Column(Integer, ForeignKey('produits_finis.id'))
    etat_production = Column(String(50))

    produit_fini = relationship('ProduitFini')
    matieres_premieres_necessaires = relationship('MatierePremiere', secondary='ordre_production_matiere_premiere_matieres_premieres')

# Table d'association OrdreProduction-MatierePremiere
ordre_production_matiere_premiere_matieres_premieres = Table('ordre_production_matiere_premiere_matieres_premieres', Base.metadata,
    Column('ordre_production_id', Integer, ForeignKey('ordres_production.id')),
    Column('matiere_premiere_id', Integer, ForeignKey('matieres_premieres.id'))
)

# Modèle Bon de Livraison
class BonLivraison(Base):
    __tablename__ = 'bons_livraison'

    id = Column(Integer, primary_key=True)
    date_livraison = Column(Date)
    client_id = Column(Integer, ForeignKey('clients.id'))

    client = relationship('Client')
    produits_livres = relationship('ProduitFini', secondary='bon_livraison_produit_fini')

# Table d'association BonLivraison-ProduitFini
bon_livraison_produit_fini = Table('bon_livraison_produit_fini', Base.metadata,
    Column('bon_livraison_id', Integer, ForeignKey('bons_livraison.id')),
    Column('produit_fini_id', Integer, ForeignKey('produits_finis.id'))
)

# Créer la base de données SQLite3
engine = create_engine('sqlite:///votre_base_de_donnees.db')
Base.metadata.create_all(engine)

# Créer une session SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()
