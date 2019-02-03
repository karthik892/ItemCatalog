from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from Database import Base, Category, Item, User
from sqlalchemy.orm import sessionmaker
import datetime

engine = create_engine('sqlite:///ItemCatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
session.merge(Category(name="Movies"))
session.merge(Category(name="Games"))
"""
# To use these sample statements you should add the line
# creator_email = <your-google-email>
# to the Item parameters so that you can edit/delete them in the application
# i.e. the creator_email column is used to determine if you can edit/delete
# an item

session.merge(Item(
    name="Harry Potter and the Deathly Hallows, Part 1",
    description="Sample description",
    category_name="Movies",
    creation_date=datetime.datetime.now()
))
session.merge(Item(
    name="Avatar",
    description="Sample description",
    category_name="Movies",
    creation_date=datetime.datetime.now()
))
session.merge(Item(
    name="Portal 2", description="Sample description", category_name="Games",
    creation_date=datetime.datetime.now()
))
session.merge(Item(
    name="Wall-E", description="Sample description", category_name="Movies",
    creation_date=datetime.datetime.now()
))
session.merge(Item(
    name="Portal", description="Sample description", category_name="Games",
    creation_date=datetime.datetime.now()
))
session.merge(Item(
    name="Black Panther",
    description="Sample description",
    category_name="Movies",
    creation_date=datetime.datetime.now()
))
session.merge(Item(
    name="Quantum Conundrum",
    description="Sample description",
    category_name="Games",
    creation_date=datetime.datetime.now()
))
session.merge(Item(
    name="Home Alone",
    description="Sample description",
    category_name="Movies",
    creation_date=datetime.datetime.now()
))
"""
session.commit()
