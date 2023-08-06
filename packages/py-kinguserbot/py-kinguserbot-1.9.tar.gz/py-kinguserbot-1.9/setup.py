import re

import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

name = "py-kinguserbot"
author = "TeamDevil"
author_email = "De.codes.official@gmail.com"
version="1.9"
description = "A Secure and Powerful Python-PyrogramBased Library For Kingbot ."
license = "GNU AFFERO GENERAL PUBLIC LICENSE (v3)"
url = "https://github.com/ToxicCyber/kinguserbot"
download_url="https://github.com/thearyanag/kingbot/archive/refs/tags/0.2.tar.gz"

setuptools.setup(
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=url,
    license=license,
    packages=setuptools.find_packages(),
    install_requires=[
        "pyrogram",
        "redis",
        "python-decouple==3.3",
        "TgCrypto==1.2.2",
        "python-dotenv==0.15.0",
        "sqlalchemy",
        "heroku3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

