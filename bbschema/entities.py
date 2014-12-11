# -*- coding: utf8 -*-

# Copyright (C) 2014  Ben Ockmore

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This module specifies a class, Resource, which is designed to be used as the
base class for all resource models specified in this package."""

from sqlalchemy import (Boolean, Column, Integer, String, DateTime,
                        UnicodeText, ForeignKey, Date, Enum)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
import sqlalchemy.sql as sql

from bbschema.base import Base
from .entity import EntityData


class PublicationData(EntityData):
    __tablename__ = 'publication_data'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, ForeignKey('bookbrainz.entity_data.id'), primary_key=True)
    book_type_id = Column(Integer, ForeignKey('bookbrainz.publication_type.id'))

    book_type = relationship('PublicationType')

    __mapper_args__ = {
        'polymorphic_identity': 1,
    }


class PublicationType(Base):
    __tablename__ = 'publication_type'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, primary_key=True)
    label = Column(UnicodeText, nullable=False, unique=True)


class CreatorData(EntityData):
    __tablename__ = 'creator_data'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, ForeignKey('bookbrainz.entity_data.id'), primary_key=True)

    begin_date = Column(Date)
    begin_date_precision = Column(
        Enum('YEAR', 'MONTH', 'DAY', name='date_precision')
    )
    end_date = Column(Date)
    end_date_precision = Column(
        Enum('YEAR', 'MONTH', 'DAY', name='date_precision')
    )
    ended = Column(Boolean, server_default='false')

    country_id = Column(Integer)
    gender_id = Column(Integer, ForeignKey('musicbrainz.gender.id'))
    creator_type_id = Column(Integer, ForeignKey('bookbrainz.book_type.id'))

    gender = relationship('Gender')
    creator_type = relationship('BookType')

    __mapper_args__ = {
        'polymorphic_identity': 2,
    }


class CreatorType(Base):
    __tablename__ = 'creator_type'
    __table_args__ = {'schema': 'bookbrainz'}

    id = Column(Integer, primary_key=True)
    label = Column(UnicodeText, nullable=False, unique=True)
