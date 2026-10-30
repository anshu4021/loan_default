@echo off
echo =====================================================================
echo    EXPLAINABLE AI LOAN DEFAULT PREDICTION - WORKING PROTOTYPE
echo =====================================================================
echo.
echo Select an execution mode:
echo [1] Launch Interactive Web Dashboard (Streamlit UI)
echo [2] Launch Command Line Interface (CLI Prototype)
echo [3] Launch REST API Service (Port 8080)
echo [4] Exit
echo.

set /p mode="Enter option (1-4): "

if "%mode%"=="1" (
    echo Starting Streamlit Web Application...
    cd ..
    streamlit run app.py
) else if "%mode%"=="2" (
    echo Starting Terminal CLI Prototype...
    python cli_prototype.py
) else if "%mode%"=="3" (
    echo Starting REST API Prototype...
    python api_prototype.py
) else (
    echo Exiting.
)
pause
