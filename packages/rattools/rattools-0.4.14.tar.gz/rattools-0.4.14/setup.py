from setuptools import setup
setup(
    name="rattools",
    version="0.4.14",
    description="Este es un paquete de ejemplo",
    author="Ldog",
    author_email="domgutluis@gmail.com",
    url="",
    packages=['rattools'],
    install_requires=[            # I get to this in a second
          'yfinance',
          'pandas',
          'sklearn',
          'matplotlib',
          'seaborn',
          'plotly',
          'pymysql',
          'logging',
          'sshtunnel']
)