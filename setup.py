from setuptools import setup, find_packages

setup(
    name='vaultflow',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'inquirerpy',
        'pyfiglet',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'vaultflow = vaultflow.cli:cli',
        ],
    },
    author='Tu Nombre',
    author_email='tu@email.com',
    description='Una herramienta CLI para gestionar Vaults de Obsidian con Git.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tu_usuario/vaultflow',
)