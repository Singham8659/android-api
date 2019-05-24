from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only
from marshmallow_sqlalchemy import ModelSchema
import json
from flask import session, redirect, url_for, jsonify
from utils import encrypt_string

db = SQLAlchemy()

####################
#Table User
####################

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String)
    passe = db.Column(db.String)
    admin = db.Column(db.Integer)
    connecte = db.Column(db.Integer)
    couleur = db.Column(db.String)
    blacklist = db.Column(db.Integer)

    def __init__(self, pseudo, passe, admin, connecte, couleur):
        self.pseudo = pseudo
        self.passe = passe
        self.admin = admin
        self.connecte = connecte
        self.blacklist = blacklist

class UserSchema(ModelSchema):
    class Meta:
        model = User

user_schema = UserSchema()

def insert_user(pseudo, passe):
    new_user = User(pseudo, encrypt_string(passe), 0, 0, 'black')
    db.session.add(new_user)
    db.session.commit()

def check_login(pseudo, passe):
    checked_user = user_schema.dump(User.query.filter_by(pseudo=pseudo).first()).data
    if not checked_user:
        return False
    elif checked_user['passe'] == encrypt_string(passe):
        return True
    else:
        return True

def is_admin(pseudo):
    user = user_schema.dump(User.query.filter_by(pseudo=pseudo).first()).data
    if not user:
        return 0
    else:
        return user["admin"]

def get_all_users():
    return user_schema.dumps(User.query.all(), many=True).data

def set_user_connected(pseudo):
    user = User.query.filter_by(pseudo=pseudo).first()
    user.connecte = 1
    db.session.commit()

def blacklist_user(pseudo):
    user = User.query.filter_by(pseudo=pseudo).first()
    user.blacklist = 1
    db.session.commit()

####################
#Table Conversation
####################

class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Integer)
    theme =  db.Column(db.String)

    def __init__(self, active, theme):
        self.active = active
        self.theme = theme

class ConversationSchema(ModelSchema):
    class Meta:
        model = Conversation

conversation_schema = ConversationSchema()

def create_new_conversation(theme):
    new_conversation = Conversation(1, theme)
    db.session.add(new_conversation)
    db.session.commit()
    return new_conversation.id

def get_all_conversations():
    return conversation_schema.dumps(Conversation.query.all(), many=True).data


####################
#Table Message
####################

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    idConversation = db.Column(db.Integer)
    idAuteur = db.Column(db.Integer)
    contenu = db.Column(db.String)

    def __init__(self, idConversation, idAuteur, contenu):
        self.idConversation = idConversation
        self.idAuteur = idAuteur
        self.contenu = contenu

class MessageSchema(ModelSchema):
    class Meta:
        model = Message

message_schema = MessageSchema()

def get_messages_by_conv(idConversation):
    return message_schema.dumps(Message.query.filter_by(idConversation=idConversation).all(), many=True).data

def insert_message(idAuteur, idConversation, content):
    new_message = Message(idConversation, idAuteur, contenu)
    db.session.add(new_message)
    db.session.commit()