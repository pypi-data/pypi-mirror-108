# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane', 'arcane.notification']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.7,<3.0']

setup_kwargs = {
    'name': 'arcane-notification',
    'version': '0.2.0',
    'description': 'Defines notification tools',
    'long_description': "# Arcane notification\n\n## Description\n\nCe package nous permet de créer des objets `Notification`, des les créer et de les valider pour ne plus les recevoir (acknowledge).\nVous pouvez trouver le [schéma d'architecture](https://docs.google.com/drawings/d/1NdC6NIW8GKa1d8wRyxe1pmVN-xA0eCiN9TCYWRjA7JI/edit) dans le drive produit.\nUne notification correspond concrètement à un mail envoyé par les cloud functions de [notification_services](https://github.com/arcane-run/smartFeeds/tree/master/common_services/notification_services).\nVous pouvez trouver dans la définition du type `Notification` les différents paramètres et leurs usages mais on peut distinguer plusieurs configurations classiques:\n\n1. Je souhaite envoyer un mail dès la création de la notification et un rappel le lendemain matin.\n\nIl suffit de mettre le paramètre `send_on_activation` à `True` pour qu'automatiquement un mail soit envoyé lors de la création de la notification (c'est à dire dans la cloud function `post_notification`).\nPour activer les rappels le matin, il faut mettre `severity` à `MEDIUM`.\nPour que les rappels cessent d'être envoyés, on peut définir une `end_date` au lendemain. Une fois la date de fin passée, une notification ne génère plus de mail.\nAttention, si le `notification_name` existe déjà, aucun mail ne sera envoyé lors du post. Par contre, la `end_date` sera décalée.\n\n2. Je souhaite envoyer un mail tous les 3 heures jusqu'à ce que l'utilisateur choisisse de ne plus recevoir la notification.\n\nPour recevoir des mails toutes les 3h, il suffit de mettre `severity` à `HIGH`.\nSur chaque email envoyé, l'utilisateur peut acknowledge une notification via l'icône de l'horloge.\n\n## FAQ\n\n- J'ai créé un nouveau mail. Comment faire en sorte de le recevoir?\n  - S'assurer que la cloud function `post_notification` existe sur le projet en question, la créer sinon.\n  - Créer une `Notification` à partir du type avec `send_on_activation` à `True`, `recipients` doit contenir uniquement votre email et `notification_name` ne doit pas déjà exister (vous pouvez regarder dans Datastore).\n  - Une fois le message pubsub envoyé avec la fonction `post_notification` vous devriez recevoir un mail.\n  - Si vous n'avez rien reçu, vous pouvez vérifier les logs de la cloud function `post_notification`. Si il n'y a pas le log `Sending alert to`, il y a un problème dans l'objet notification que vous avez envoyé. Si le log est présent mais que vous ne recevez rien, il est possible que le problème vienne de [mailjet](https://www.mailjet.com/).\n",
    'author': 'Arcane',
    'author_email': 'product@arcane.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
