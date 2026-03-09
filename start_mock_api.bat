@echo off
REM Start Mock API Server
echo Starting Mock API Server...
echo Mock API Server will run on http://127.0.0.1:48080
echo Press Ctrl+C to stop the server
echo.

python mock_api\server.py
