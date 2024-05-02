@echo off
echo Have you placed storepage_base.json and appname_base.json into the source folder? 
set /p ready="Press any key when ready"
python translateStorePages.py
python translateStoreNames.py

set /p ready="Done"