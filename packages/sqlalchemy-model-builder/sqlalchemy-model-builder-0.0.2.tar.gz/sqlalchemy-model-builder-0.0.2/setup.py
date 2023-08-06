# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_model_builder']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy==1.4.0']

setup_kwargs = {
    'name': 'sqlalchemy-model-builder',
    'version': '0.0.2',
    'description': 'SQLAlchemy Model Builder',
    'long_description': '# SQLAlchemy Model Builder\n![test](https://github.com/aminalaee/sqlalchemy-model-builder/actions/workflows/test.yml/badge.svg) ![publish](https://github.com/aminalaee/sqlalchemy-model-builder/actions/workflows/publish.yml/badge.svg) [![codecov](https://codecov.io/gh/aminalaee/sqlalchemy-model-builder/branch/main/graph/badge.svg?token=QOLK6R9M52)](https://codecov.io/gh/aminalaee/sqlalchemy-model-builder) \n[![pypi](https://img.shields.io/pypi/v/sqlalchemy-model-builder?color=%2334D058&label=pypi)](https://pypi.org/project/sqlalchemy-model-builder/)\n\n## Features\n- Build and Save SQLALchemy models with random data\n- Build relationships (Todo)\n- Build with minimal (required) fields only (Todo)\n\n## How to use\nBuild SQLAlchemy model:\n```\nfrom sqlalchemy.ext.declarative import declarative_base\nfrom sqlalchemy.sql.sqltypes import Integer, String\n\nfrom sqlalchemy_model_builder import ModelBuilder\n\nBase = declarative_base()\n\n\nclass User(Base):\n    __tablename__ = "users"\n\n    id = Column(Integer, primary_key=True)\n    name = Column(String)\n\n\nrandom_user = ModelBuilder(User).build()  # Note: This will not insert the User\n```\n\nSave SQLAlchemy model:\n```\nfrom sqlalchemy.ext.declarative import declarative_base\nfrom sqlalchemy.sql.sqltypes import Integer, String\n\nfrom sqlalchemy_model_builder import ModelBuilder\n\nBase = declarative_base()\n\nengine = create_engine("sqlite://", echo=True)\n\n\nclass User(Base):\n    __tablename__ = "users"\n\n    bio = Column(Text)\n    id = Column(Integer, primary_key=True)\n    name = Column(String)\n\n\nBase.metadata.create_all(engine)\n\nLocalSession = sessionmaker(bind=engine)\n\ndb = LocalSession()\n\n\nrandom_user = ModelBuilder(User).save(db=db)  # Note: Builds and Saves model using provided session\n```\n\n## Supported Data Types\n- BigInteger\n- Boolean\n- Date\n- DateTime\n- Enum  (Todo)\n- Float\n- Integer\n- Interval\n- LargeBinary (Todo)\n- MatchType (Todo)\n- Numeric (Todo)\n- PickleType (Todo)\n- SchemaType (Todo)\n- SmallInteger\n- String\n- Text\n- Time\n- Unicode\n- UnicodeText\n',
    'author': 'Amin Alaee',
    'author_email': 'mohammadamin.alaee@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aminalaee/sqlalchemy-model-builder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
