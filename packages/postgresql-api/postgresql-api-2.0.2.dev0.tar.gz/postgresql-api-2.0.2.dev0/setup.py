from setuptools import setup

with open("README.rst") as rst:
    description = rst.read()

setup(
    name="postgresql-api",
    version="2.0.2.dev0",
    packages=["postgresql_api"],
    url="https://github.com/AlexDev-py/postgresql_api.git",
    license="MIT",
    author="AlexDev",
    author_email="aleks.filiov@yandex.ru",
    description="API for postgresql",
    long_description=description,
    install_requires=["psycopg2"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)

# sdist
# twine register dist/postgresql-api-2.0.1.tar.gz
# twine upload dist/postgresql-api-2.0.1.tar.gz
# -r testpypi
