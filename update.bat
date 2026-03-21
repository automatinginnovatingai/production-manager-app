@echo off
timeout /t 5

taskkill /f /im "Production Manager App.exe"

move /Y "update.exe" "Production Manager App.exe"

start "" "Production Manager App.exe"