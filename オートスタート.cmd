@echo off

call venv\Scripts\activate
python get_all_products.py
python get_all_instruction_manuals.py
python get_cover_image.py
start 取扱い説明書一覧.html