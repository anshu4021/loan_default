#!/bin/bash
echo "====================================================================="
echo "   EXPLAINABLE AI LOAN DEFAULT PREDICTION - WORKING PROTOTYPE"
echo "====================================================================="
echo ""
echo "Select an execution mode:"
echo "1) Launch Interactive Web Dashboard (Streamlit UI)"
echo "2) Launch Command Line Interface (CLI Prototype)"
echo "3) Launch REST API Service (Port 8080)"
echo "4) Exit"
echo ""

read -p "Enter option (1-4): " mode

if [ "$mode" = "1" ]; then
    echo "Starting Streamlit Web Application..."
    cd .. && streamlit run app.py
elif [ "$mode" = "2" ]; then
    echo "Starting Terminal CLI Prototype..."
    python cli_prototype.py
elif [ "$mode" = "3" ]; then
    echo "Starting REST API Prototype..."
    python api_prototype.py
else
    echo "Exiting."
fi
