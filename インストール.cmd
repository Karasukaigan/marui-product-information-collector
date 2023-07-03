@echo off

chcp 65001 > nul
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt