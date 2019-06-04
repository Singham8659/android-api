<h1>Instructions d'installation</h1>

<h2>Prérequis</h2>

Pour faire fonctionner ce projet il vous faudra:
- pip (utilitaire python). Si vous ne l'avez pas cliquez <a target="_blank" href="https://pip.pypa.io/en/stable/installing/">ici</a>
- le module virtualenv que vous trouverez <a target="_blank" href="https://virtualenv.pypa.io/en/latest/installation/">ici</a>

<h2>Étape 1: clonez le repo</h2>

Clonez ce repository localement

<h2>Étape 2: créez votre virtualenv</h2>

- Rendez vous à la racine de votre répertoire fraîchement créé.
- exécutez la commande <strong>"virtualenv ."</strong> Cela fera de votre répertoire un virtualenv vous permettant d'installer des modules python
- Activez le virtualenv: Vous constaterez la présence d'un répertoire "Scripts" dans votre virtualenv. 
  exécutez donc la commande <strong>./Scripts/activate</strong>

L'activation du virtualenv est absolument nécessaire pour la suite des opérations.

<h2>Étape 3: installez les modules nécessaires grâce à pip</h2>
- Une fois le virtualenv activé, exécutez la commande <strong>pip install -r requirements.txt</strong>
- Cela installera les modules nécessaires à notre application.

<h2>Étape 4: initialisez une variable d'environnement</h2>
- exécutez la commande <strong>export FLASK_APP=app.py</strong>

<h2>Étape 5: Importer la base de données modifiée</h2>
<ul>
  <li>- télécharger le ficher base.sql fourni sur ce dépot git</li>
  <li>- le champ mot de passe a été modifié pour accueillir un mot de passe crypté</li>
  <li>- importer ce fichier dans une base SQL locale (MySQL)</li>
  <li>- il est nécessaire que la base s'appelle "android_chat"</li>
  <li>- On peut modifier la configuration de l'accès à la base dans le fichier app.py (variable db_conn)</li>
  <li>- modèle à suivre: <strong>mysql+pymysql://login:mdp@localhost/nom_bdd</strong></li>
  <li>- les mots de passes de Tom et Jean-Pierre sont cryptés, il correspondent aux anciens mots de passe (tomtom et tintin)</li>
</ul>

<h2>Étape 6: démarrez l'application</h2>
- exécutez la commande <strong>python -m flask run</strong>
- L'application est maintenant démarrée
-Ctrl C pour arrêter l'application, et <strong>./Scripts/deactivate</strong> pour désactiver le virtualenv
-L'application va être accessible depuis l'adresse localhost:5000 par défaut






