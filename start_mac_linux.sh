#!/bin/bash

echo "============================"
echo "          EduGenie"
echo "============================"

echo ""

if [ ! -d ".venv" ]; then

    echo "Creating virtual environment..."

    python3 -m venv .venv

fi


echo "Activating environment..."

source .venv/bin/activate


echo "Installing dependencies..."

python -m pip install --upgrade pip

pip install -r requirements.txt


if [ ! -f ".env" ]; then

    cp .env.example .env

    echo ""
    echo ".env created."
    echo "Add your Gemini API key."
    echo ""

fi


echo "Starting EduGenie..."

uvicorn main:app --reload