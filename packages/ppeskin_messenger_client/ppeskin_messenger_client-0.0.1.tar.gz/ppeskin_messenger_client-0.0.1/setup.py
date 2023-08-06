from setuptools import setup, find_packages

setup(name="ppeskin_messenger_client",
      version="0.0.1",
      description="ppeskin_messenger_client",
      author="Pavel Peskin",
      author_email="ppeskin@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
