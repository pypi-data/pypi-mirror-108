# Hello from Wouter

Just a basic example package to test uploading to pypi

## Building steps

```
apt-get install python3-venv

python3 -m pip install --upgrade build twine
python3 -m build
python3 -m twine upload dist/*
```

## Usage 
```
pip3 install example-pkg-dankersw
```
```python
from example_pkg import hi_example

obj = hi_example
```