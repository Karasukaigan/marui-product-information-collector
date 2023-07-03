@echo off

python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
pip freeze > requirements.txt