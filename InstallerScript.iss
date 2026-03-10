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

; Add SQL Server Express installer to payload
Source: "InstallerPayload\SQLEXPR_x64_ENU.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Icons]
Name: "{group}\Production Manager App SQL Server Express"; Filename: "{app}\Production Manager App SQL Server Express.exe"; IconFilename: "{app}\photo.ico"
Name: "{commondesktop}\Production Manager App SQL Server Express"; Filename: "{app}\Production Manager App SQL Server Express.exe"; IconFilename: "{app}\photo.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Run]
; Install SQL Server Express silently
Filename: "{tmp}\SQLEXPR_x64_ENU.exe"; \
    Parameters: "/QS /ACTION=Install /FEATURES=SQLEngine /INSTANCENAME=MYAPP /SQLSVCACCOUNT=""NT AUTHORITY\NETWORK SERVICE"" /TCPENABLED=1 /IACCEPTSQLSERVERLICENSETERMS"; \
    StatusMsg: "Installing SQL Server Express..."; \
    Flags: waituntilterminated

; Launch your app after SQL Express is installed
Filename: "{app}\Production Manager App SQL Server Express.exe"; Description: "Launch Production Manager App SQL Server Express"; Flags: nowait postinstall skipifsilent
Filename: "{app}\README.txt"; Description: "View README"; Flags: postinstall shellexec skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{userappdata}\Production Manager App SQL Server Express"