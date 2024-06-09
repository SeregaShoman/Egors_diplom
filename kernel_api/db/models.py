import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, Text, ARRAY, func, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import BASE


def generate_uuid():
    return str(uuid.uuid4())


class Role(BASE):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    users = relationship('User', order_by='User.id', back_populates='role')


class User(BASE):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    fio = Column(String(100), nullable=False)
    avatar_url = Column(String(255))
    login = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship('Role', back_populates='users')
    events_created = relationship('Event', back_populates='creator')
    student_info = relationship('Student', uselist=False, back_populates='user')
    partner_info = relationship('Partner', uselist=False, back_populates='user')


class Student(BASE):
    __tablename__ = 'students'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    groups = Column(String(100), nullable=False)
    institution = Column(String(100), nullable=False)

    user = relationship('User', back_populates='student_info')


class Partner(BASE):
    __tablename__ = 'partners'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    organization = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)

    user = relationship('User', back_populates='partner_info')


class Event(BASE):
    __tablename__ = 'events'
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    max_participants = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)
    start_time = Column(DateTime, nullable=False)
    created_time = Column(DateTime, nullable=False, default=datetime.now)
    image_url = Column(String(255))
    creator_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    creator = relationship('User', back_populates='events_created')
    registrations = relationship('EventRegistration', back_populates='event')


class EventRegistration(BASE):
    __tablename__ = 'eventregistrations'
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    event_id = Column(UUID(as_uuid=True), ForeignKey('events.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    event = relationship('Event', back_populates='registrations')
    user = relationship('User')


class Tags(BASE):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partners_items = Column(ARRAY(String), nullable=False)
    education_items = Column(ARRAY(String), nullable=False)
    organization_items = Column(ARRAY(String), nullable=False)
