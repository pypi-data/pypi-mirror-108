# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blagues_api']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7,<4.0', 'pydantic>=1.8,<2.0']

setup_kwargs = {
    'name': 'blagues-api',
    'version': '1.0.0',
    'description': 'Official client for Blagues API',
    'long_description': '# BlaguesAPI Python\n\nCe paquet Python fournit une interface simple pour intéragir avec [Blagues API](https://www.blagues-api.fr/).  \n**Important :** Ce paquet ne fournit que des méthodes **asynchrones**.\n\n## Installation\n\nVous pouvez simplement ajouter la dépendance à votre projet depuis PyPI :\n```\npip install blagues_api\n```\n\n## Utilisation\n\nPour utiliser l\'API, vous devez obtenir une clé gratuite sur le site officiel : https://www.blagues-api.fr/. Vous pourrez ensuite construire un objet `BlaguesAPI` :\n\n```py\nfrom blagues_api import BlaguesAPI\n\nblagues = BlaguesAPI("VOTRE_TOKEN_ICI")\n```\n\nToutes les méthodes renverront un objet `Blagues`, qui permet d\'accéder aux différentes propriétés renvoyées par l\'API : `id`, `type`, `joke`, `answer`. En cas d\'erreur, vous recevrez une erreur du type [`aiohttp.ClientResponseError`](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientResponseError).\n\nLes différents types de blagues peuvent être représentés au choix sous forme d\'un string ou d\'un objet `BlagueType` (exemple: `BlagueType.GENERAL`). La liste des types disponibles est notée dans sur le site officiel.\n\n### Blague aléatoire\n\n```py\nawait blagues.random()\n# Blague(id=108, type=<BlagueType.GLOBAL: \'global\'>, joke="C\'est l\'histoire d\'un poil. Avant, il était bien.", answer=\'Maintenant, il est pubien.\')\n```\n\nIl est possible de spécifier des catégories à exclure :\n```py\nawait blagues.random(disallow=[BlagueType.LIMIT, BlagueType.BEAUF])\n\n# Avec des strings\nawait blagues.random(disallow=["limit", "beauf"])\n```\n\n### Blague aléatoire catégorisée\n\n```py\nawait blagues.random_categorized(BlagueType.DEV)\n# Blague(id=430, type=<BlagueType.DEV: \'dev\'>, joke=\'De quelle couleur sont tes yeux ?\', answer=\'#1292f4 et toi ?\')\n\n# Avec des strings\nawait blagues.random_categorized("dev")\n```\n\n### Blague par identifiant\n\n```py\nawait blagues.from_id(20)\n# Blague(id=20, type=<BlagueType.GLOBAL: \'global\'>, joke="Qu\'est-ce qu\'un chou au milieu de l\'océan ?", answer=\'Un chou marin.\')\n```',
    'author': 'baptiste0928',
    'author_email': 'contact@baptiste0928.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.blagues-api.fr/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
