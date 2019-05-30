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

<h2>Étape 5: démarrez l'application</h2>
- exécutez la commande <strong>python -m flask run</strong>
- L'application est maintenant démarrée
-Ctrl C pour arrêter l'application, et <strong>./Scripts/deactivate</strong> pour désactiver le virtualenv
-L'application va être accessible depuis l'adresse localhost:5000 par défaut

<h2>Étape 6: priez</h2>
priez pour que ça marche





