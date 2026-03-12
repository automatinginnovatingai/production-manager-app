; InstallerScript.iss

[Setup]
AppName=Production Manager App SQL Server Express
AppVersion=1.0.1
DefaultDirName={autopf}\Production Manager App SQL Server Express
DefaultGroupName=Production Manager App SQL Server Express
OutputBaseFilename=Production_Manager_App_SQL_Server_Express_Installer_v1.0.1
OutputDir=installer_build
SetupIconFile=photo.ico
Compression=lzma
SolidCompression=yes
LicenseFile=InstallerPayload\LICENSE.txt
PrivilegesRequired=admin

[Files]
Source: "InstallerPayload\Production Manager App SQL Server Express.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "InstallerPayload\README.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "InstallerPayload\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "InstallerPayload\photo.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "InstallerPayload\SQLEXPRESS_EXTRACTED\*"; DestDir: "{tmp}\SQLEXPRESS_EXTRACTED"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Production Manager App SQL Server Express"; Filename: "{app}\Production Manager App SQL Server Express.exe"; IconFilename: "{app}\photo.ico"
Name: "{commondesktop}\Production Manager App SQL Server Express"; Filename: "{app}\Production Manager App SQL Server Express.exe"; IconFilename: "{app}\photo.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
Filename: "{tmp}\SQLEXPRESS_EXTRACTED\setup.exe"; \
    Parameters: "/QS /ACTION=Install /FEATURES=SQLEngine /INSTANCENAME=SQLEXPRESS /TCPENABLED=1 /NPENABLED=1 /IACCEPTSQLSERVERLICENSETERMS"; \
    Flags: waituntilterminated

; Force-enable TCP/IP
Filename: "reg.exe"; \
    Parameters: "add ""HKLM\SOFTWARE\Microsoft\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQLServer\SuperSocketNetLib\Tcp"" /v Enabled /t REG_DWORD /d 1 /f"; \
    Flags: runhidden waituntilterminated

; Force-enable Named Pipes
Filename: "reg.exe"; \
    Parameters: "add ""HKLM\SOFTWARE\Microsoft\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQLServer\SuperSocketNetLib\Np"" /v Enabled /t REG_DWORD /d 1 /f"; \
    Flags: runhidden waituntilterminated

; Restart SQL Server service
Filename: "sc.exe"; Parameters: "stop MSSQL$SQLEXPRESS"; Flags: runhidden waituntilterminated
Filename: "sc.exe"; Parameters: "start MSSQL$SQLEXPRESS"; Flags: runhidden waituntilterminated

; Launch app
Filename: "{app}\Production Manager App SQL Server Express.exe"; Flags: nowait postinstall skipifsilent
Filename: "{app}\README.txt"; Flags: postinstall shellexec skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{userappdata}\Production Manager App SQL Server Express"