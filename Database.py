import sys
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy import String, Boolean, Numeric, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Category(Base):
    __tablename__ = "category"
    name = Column(String(50), primary_key=True)


class Item(Base):
    __tablename__ = "item"
    name = Column(String(50), primary_key=True)
    description = Column(String(1000))
    category_name = Column(String(50), ForeignKey("category.name"))
    creation_date = Column(DateTime())
    creator_email = Column(String(255))
    category = relationship(Category)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'category_name': self.category_name,
            'creation_date': self.creation_date
        }


class User(Base):
    __tablename__ = "User"
    email = Column(String(255), primary_key=True)
    name = Column(String(255))

engine = create_engine('postgresql://scott:tiger@localhost:5432/mydatabase')
Base.metadata.create_all(engine)
