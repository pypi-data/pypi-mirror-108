from setuptools import setup, find_packages
from pathlib import Path


def long_description():
    return Path("./README.md").read_text()


author_email = 'satyamsoni@hotmail.co.uk'
setup(name='crypto_data_fetcher',
      version='1.0.0',
      description='Utilities for fetching Crypto Coin data',
      author='Satyam Soni',
      author_email=author_email,
      maintainer="Satyam Soni",
      maintainer_email=author_email,
      packages=find_packages(),
      package_dir={"crypto_data_fetcher": "crypto_data_fetcher"},
      url="https://gitlab.com/satyamsoni2211/cryptodatafetcher",
      keywords=[
          "Bitcoin",
          "crypto",
          "crypto currency",
          "dodge coin",
          "coin"
      ],
      install_requires=(
          "aiohttp==3.7.4",
      ),
      extras_require={
          "dev": ["sphinx", "sphinx-rtd-theme==0.5.2", "sphinx-markdown-builder"]
      },
      platforms="Platform Independent",
      long_description=long_description(),
      long_description_content_type="text/markdown"
      )
