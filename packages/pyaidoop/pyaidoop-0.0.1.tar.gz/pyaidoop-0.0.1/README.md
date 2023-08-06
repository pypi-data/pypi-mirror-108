# pyaidoop
aidoop python package module

## Setup
### setup commands
```
pip install -r requirements.txt
pip install --upgrade pip
python setup.py install
python setup.py sdist bdist_wheel
pip install -r requirements.txt
python -m twine upload --repository testpypi dist/*
```