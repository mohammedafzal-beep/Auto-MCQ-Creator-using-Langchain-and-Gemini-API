from setuptools import find_packages,setup

setup(
    name='mcqgenrator',
    version='0.0.1',
    author='Mohammed Afzal',
    author_email='mhdafz9@gmail.com',
    install_requires=["hugginface_hub","streamlit","PyPDF2"],
    packages=find_packages()
)