from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
from base import db
from base import (get_all_users, check_login, is_admin, get_all_conversations, 
                get_messages_by_conv, create_new_conversation, get_last_messages_by_conv, 
                set_user_connected, is_blacklisted, blacklist_user, insert_message,
                get_user_info, check_identity, delete_message_by_id,
                insert_user, delete_user_by_id, login_dispo, check_author_identity,
                delete_conversation_by_id)
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity, verify_jwt_in_request, get_jwt_claims, get_raw_jwt)
import sys
import pymysql
from functools import wraps

app = Flask(__name__)
app.secret_key = "secret-key"
app.config['JWT_SECRET_KEY'] = "secret-jwt-key"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
jwt = JWTManager(app)
CORS(app)

db_conn = 'mysql+pymysql://root:@localhost/android_chat'
app.config['SQLALCHEMY_DATABASE_URI'] = db_conn

blacklist = set()

with app.app_context():
    db.init_app(app)
    db.create_all()

#Cette annotation sert à ajouter la donnée "admin" de l'utilisateur dans le claim du token
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        'admin' : is_admin(identity)
    }

#annotation personnalisée permettant de réserver un chemin aux admins seulement
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['admin'] != 1:
            return jsonify(msg='Admins only!'), 403
        else:
            return fn(*args, **kwargs)
    return wrapper

#annotation permettant de vérifier la présence d'un token dans la blacklist (déconnexion)
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

@app.route('/')
def hello_world():
    return 'Hello, World!'

#chemin permettant de récupérer tous les utilisateurs
@app.route('/users', methods=['GET'])
@admin_required
def get_users():
    return get_all_users()

#inscription de l'utilisateur
#envoyer objet json de type {"login":login, "password":password}
@app.route('/signup', methods=['POST'])
def signup():
    post_data = request.get_json()
    login = post_data["login"]
    password = post_data["password"]
    if not login_dispo(login):
        return jsonify({"status": "failure", "message":"pseudo non disponible"}), 400
    insert_user(login, password)
    access_token = create_access_token(identity = login)
    return jsonify({"status":"success", "message":"utilisateur ajouté", "token": access_token}), 200
    

#chemin de login (envoyer json avec login et password)
@app.route('/login', methods=['POST'])
def login():
    post_data = request.get_json()
    login = post_data["login"]
    password = post_data["password"]
    if not login or not password:
        return jsonify({"status":"failure", "message":"Entrez toutes les informations nécessaires SVP"}), 400
    if is_blacklisted(login):
        return jsonify({"status":"failure", "message":"Vous avez été blacklisté"}), 400
    elif check_login(login, password):
        access_token = create_access_token(identity = login)
        set_user_connected(login, 1)
        userInfo = get_user_info(login)
        return jsonify({'status': 'success', 'message': 'connexion réussie', 'token': access_token, 'userInfo': userInfo}), 200
    else:
        return jsonify({'status': 'failure', 'message': 'votre mot de passe ou votre pseudo est faux'}), 400

#chemin de déconnexion, on ajoute le token de l'utilisateur dans la blacklist
#afin d'empêcher son utilisation
@app.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    pseudo = get_jwt_identity()
    set_user_connected(pseudo, 0)
    print(get_raw_jwt(), file=sys.stderr)
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"message": "déconnexion réussie"}), 200

#suppression d'utilisateur
#objet json {"userId": userId}
@app.route('/user/<id>', methods=['DELETE'])
@jwt_required
def delete_user(id):
    if not check_identity(get_jwt_identity(), id):
        return jsonify({'message': 'utilisateur non supprimé'}), 400
    delete_user_by_id(id)
    return jsonify({'message': 'utilisateur supprimé avec succès'}), 200

#on ajoute une conversation (envoyer objet json avec variable theme)
@app.route('/conversation/new', methods=['POST'])
@jwt_required
def create_conversation():
    post_data = request.get_json()
    theme = post_data["theme"]
    idConversation = create_new_conversation(theme)
    return jsonify({"status": "success", "message": "conversation créée avec succès", "idConversation": idConversation})

#charger tous les messages de la conversation d'id "conversation_id"
@app.route('/conversations/<conversation_id>', methods=['GET'])
@jwt_required
def get_messages_by_conversation(conversation_id):
    return get_messages_by_conv(conversation_id)

#cette route renvoie tous les messages de la conversation d'id conversation_id, ayant un id supérieur à message_id
@app.route('/refresh/<conversation_id>/<last_message_id>', methods=['GET'])
@jwt_required
def get_last_messages_by_conversation(conversation_id, last_message_id):
    return get_last_messages_by_conv(conversation_id, last_message_id)

#récupérer les conversations
@app.route('/conversations', methods=['GET'])
@jwt_required
def get_conversations():
    return get_all_conversations()

#envoi d'un message à la conversation idConversation (donnée dans chemin)
#envoyer objet json de type {"content": content}
@app.route('/conversation/<idConversation>/message', methods=['POST'])
@jwt_required
def send_message(idConversation): 
    post_data = request.get_json()
    content = post_data["content"]
    message = insert_message(get_jwt_identity(), idConversation, content)
    return jsonify({'message':'message envoyé', 'insertedMessage': message}), 200

@app.route('/conversation/<id>', methods=['DELETE'])
@jwt_required
def delete_conversation(id):
    if not get_jwt_claims()['admin']:
        return jsonify({'message': 'conversation non supprimée'})
    delete_conversation_by_id(id)
    return jsonify({'message': 'conversation supprimée avec succès'})

#suppression d'un message (DELETE)
@app.route('/message/<id>', methods=['DELETE'])
@jwt_required
def delete_message(id):
    claims = get_jwt_claims()
    if not check_author_identity(get_jwt_identity(), id, claims["admin"]):
        return jsonify ({'message': 'message non supprimé'}), 400
    delete_message_by_id(id)
    return jsonify({'message': 'message supprimé avec succès'}), 200

#route qui blackliste les utilisateurs.
#envoyer requete get à la route "/blacklist/idUtilisateur/blacklisté" blacklisté étant 0 ou 1
#route réservée aux admins
@app.route('/blacklist/<id>/<blacklist>', methods=['GET'])
@admin_required
def blacklist_user_by_id(id, blacklist):
    if blacklist != 0 and blacklist !=1:
        return jsonify({'message':'mauvaises valeurs', 'status':'failure'}), 400
    blacklist_user(id, blacklist)
    return jsonify({'message':'utilisateur blacklisté', 'status':'success'}), 200

@app.route('/test', methods=['GET'])
@jwt_required
def token_test():
    claims = get_jwt_claims()
    return jsonify(claims)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)