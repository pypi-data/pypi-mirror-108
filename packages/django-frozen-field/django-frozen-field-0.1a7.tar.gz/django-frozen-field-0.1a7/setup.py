# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['frozen_field']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.2,<4.0']

setup_kwargs = {
    'name': 'django-frozen-field',
    'version': '0.1a7',
    'description': 'Django model field used to store snapshot of data.',
    'long_description': '# Django Frozen Field\n\nDjango model custom field for storing a frozen snapshot of an object.\n\n## Principles\n\n* Behaves _like_ a `ForeignKey` but the data is detached from the related object\n* Transparent to the client - it looks like the original object\n* The frozen object cannot be edited\n* The frozen object cannot be saved\n\n## Usage\n\nA frozen field can be declared like a `ForeignKey`:\n\n```python\nclass Profile(Model):\n\n    address = FrozenObjectField(\n        Address,              # The model being frozen - used in validation\n        include=[],           # defaults to all non-related fields if not set\n        exclude=["line_2"],   # remove from set of fields to serialize\n        select_related=[]     # add related fields to serialization\n    )\n...\n\n>>> profile.address = Address.objects.get(...)\n>>> profile.address\n"29 Acacia Avenue"\n>>> profile.save()\n>>> type(profile.address)\nAddress\n# When fetched from the db, the property becomes a frozen instance\n>>> profile.refresh_from_db()\n>>> type(profile.address)\ntypes.FrozenAddress\n>>> profile.address.line_1\n"29 Acacia Avenue"\n>>> dataclasses.asdict(profile.address)\n{\n    "meta": {\n        "pk": 1,\n        "model": "Address",\n        "frozen_at": "...",\n        "fields": {\n            "id": "django.db.models.AutoField",\n            "line_1": "django.db.models.CharField",\n            "line_2": "django.db.models.CharField"\n        },\n        "include": ["id", "line_1"],\n        "exclude": ["line_2"],\n    },\n    "id": 1,\n    "line_1": "29 Acacia Avenue"\n}\n>>> profile.address.id\n1\n>>> profile.address.id = 2\nFrozenInstanceError: cannot assign to field \'id\'\n>>> profile.address.save()\nAttributeError: \'FrozenAddress\' object has no attribute \'save\'\n```\n\n### Controlling serialization\n\nBy default only top-level attributes of an object are frozen - related objects\n(`ForeignKey`, `OneToOneField`) are ignored. This is by design - as deep\nserialization of recursive relationships can get very complex very quickly, and\na deep serialization of an object tree is not recommended. This library is\ndesigned for the simple \'freezing\' of basic data. The recommended pattern is to\nflatten out the parts of the object tree that you wish to record. You can\ncontrol which top-level fields are included in the frozen data using the\n`include` and `exclude` arguments. Note that these are mutually exclusive - by\ndefault both are an empty list, which results in all top-level non-related\nattributes being serialized. If `included` is not empty, then *only* the fields\nin the list are serialized. If `excluded` is not empty then all fields *except*\nthose in the list are serialized.\n\nThat said, there is limited support for related object capture using the\n`select_related` argument. This currently only supports one level of child\nobject serialization, but could be extended in the future to support Django ORM\n`parent__child` style chaining of fields.\n\n## How it works\n\nThe internal wrangling of a Django model to a JSON string is done using dynamic\ndataclasses, created on the fly using the `dataclasses.make_dataclass` function.\nThe new dataclass contains one fixed property, `meta`, which is itself an\ninstance of a concrete dataclass, `FrozenObjectMeta`. This ensures that each\nserialized blob contains enought original model field metadata to be able to\ndeserialize the JSONField back into something that resembles the original. This\nis required because the process of serializing the data as JSON will convert\ncertain unsupported datatypes (e.g. `Decimal`, `float`, `date`, `datetime`,\n`UUID`) to string equivalents, and in order to deserialize these values we need\nto know what type the original value was. This is very similar to how Django\'s\nown `django.core.serializers` work.\n\n#### Running tests\n\nThe tests use `pytest` as the test runner. If you have installed the `poetry` evironment, you can run them using:\n\n```\n$ poetry run pytest\n```\n',
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': 'YunoJuno',
    'maintainer_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-frozen-data',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
