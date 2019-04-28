@echo off
pip install -r requirements.txt
python -m pip install --upgrade pip
start http://127.0.0.1:5000/
flask run