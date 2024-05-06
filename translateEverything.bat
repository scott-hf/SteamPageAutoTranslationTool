@echo off
echo Have you placed storepage_base.json and appname_base.json into the source folder? 
set /p ready="Press enter/return when ready"
mkdir temp
python pip install googletrans --upgrade
python translateStorePages.py
python translateStoreNames.py

set /p ready="Done. Press enter to close this window"