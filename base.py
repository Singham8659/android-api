from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only, joinedload, subqueryload, join
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
import json
from flask import session, redirect, url_for, jsonify
from utils import encrypt_string
import pprint
import sys

db = SQLAlchemy()

####################
#Table User
####################

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(25))
    passe = db.Column(db.String(100))
    admin = db.Column(db.Integer)
    connecte = db.Column(db.Integer)
    couleur = db.Column(db.String(50))
    blacklist = db.Column(db.Integer)

    def __init__(self, pseudo, passe, admin, couleur):
        self.pseudo = pseudo
        self.passe = passe
        self.admin = admin
        self.connecte = 1
        self.blacklist = 0
        self.couleur = couleur

class UserSchema(ModelSchema):
    class Meta:
        model = User

user_schema = UserSchema()

def insert_user(pseudo, passe):
    new_user = User(pseudo, encrypt_string(passe), 0, 'black')
    db.session.add(new_user)
    db.session.commit()

def check_login(pseudo, passe):
    checked_user = user_schema.dump(User.query.filter_by(pseudo=pseudo).first()).data
    if not checked_user:
        return False
    elif checked_user['blacklist'] == 1:
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

def is_blacklisted(pseudo):
    user = User.query.filter_by(pseudo=pseudo).first()
    return (user.blacklist == 1)

def get_all_users():
    return user_schema.dumps(User.query.all(), many=True).data

def set_user_connected(pseudo, connected):
    user = User.query.filter_by(pseudo=pseudo).first()
    user.connecte = connected
    db.session.commit()


def blacklist_user(id, blacklist):
    user = User.query.filter_by(id=id).first()
    user.blacklist = blacklist
    db.session.commit()

def get_user_info(pseudo):
    return user_schema.dump(User.query.filter_by(pseudo=pseudo).options(load_only("id", "pseudo")).first()).data

def check_identity(pseudo, id):
    user = User.query.filter_by(pseudo=pseudo).options(load_only('id', 'admin')).first()
    return (user.id == id or user.admin == 1)

def delete_user_by_id(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()

def login_dispo(pseudo):
    user = User.query.filter_by(pseudo=pseudo).first()
    return user is None

####################
#Table Conversation
####################

class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Integer)
    theme =  db.Column(db.String(100))

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
    idAuteur = db.Column(db.Integer, db.ForeignKey('users.id'))
    auteur = db.relationship("User", backref="users", lazy="joined")
    contenu = db.Column(db.String(500))

    def __init__(self, idConversation, idAuteur, contenu):
        self.idConversation = idConversation
        self.idAuteur = idAuteur
        self.contenu = contenu

class MessageSchema(ModelSchema):
    class Meta:
        model = Message
    auteur = fields.Nested(UserSchema)

message_schema = MessageSchema()

def get_messages_by_conv(idConversation):
    return message_schema.dumps(Message.query.filter_by(idConversation=idConversation).all(), many=True).data

def get_last_messages_by_conv(idConversation, lastMessageId):
    messages_list = Message.query.filter((Message.id > lastMessageId) & (Message.idConversation == idConversation)).all()
    if not messages_list:
        return jsonify({'lastMessageId': lastMessageId, 'messages': []})
    new_last_message_id = messages_list[len(messages_list) - 1].id
    messages = message_schema.dump(messages_list, many=True).data
    return jsonify({'lastMessageId' : new_last_message_id, 'messages': messages})

def insert_message(pseudo, idConversation, content):
    user = User.query.filter_by(pseudo=pseudo).first()
    new_message = Message(idConversation, user.id, content)
    db.session.add(new_message)
    db.session.commit()
    return message_schema.dump(new_message).data

def delete_message_by_id(idMessage):
    message = Message.query.filter_by(id=idMessage).first()
    db.session.delete(message)
    db.session.commit()

def check_author_identity(pseudo, idMessage, admin):
    message = Message.query.filter_by(id=idMessage).first()
    print(message.auteur.pseudo, file=sys.stderr)
    print(pseudo, file=sys.stderr)
    return (pseudo == message.auteur.pseudo or admin == 1)