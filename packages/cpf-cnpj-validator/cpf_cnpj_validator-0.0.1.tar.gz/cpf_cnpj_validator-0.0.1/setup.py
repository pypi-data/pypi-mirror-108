from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Verify if CPF or CNPJ is correct or not'
setup(
        name="cpf_cnpj_validator", 
        version=VERSION,
        author="guizin1",
        author_email="gui@abc642.net",
        description=DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
)
