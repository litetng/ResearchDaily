@echo off
cd /d "%~dp0"

call "D:\Anaconda\Scripts\activate.bat" base

start "" /B python -m streamlit run app.py

ping 127.0.0.1 -n 4 > nul


