@echo off
timeout /t 5

taskkill /f /im "Production Manager App SQL Server Express.exe"

move /Y "update.exe" "Production Manager App SQL Server Express.exe"

start "" "Production Manager App SQL Server Express.exe"