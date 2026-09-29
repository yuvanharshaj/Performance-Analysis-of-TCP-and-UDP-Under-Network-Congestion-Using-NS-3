@echo off
REM run_dashboard.bat - Launch the Streamlit dashboard on Windows
echo Starting NS-3 TCP/UDP Congestion Dashboard...
cd /d "%~dp0\.."
python -m streamlit run app/app.py
pause
