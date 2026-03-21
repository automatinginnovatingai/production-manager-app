; InstallerScript.iss

[Setup]
AppName=Production Manager App
AppVersion=1.0.0
DefaultDirName={autopf}\Production Manager App
DefaultGroupName=Production Manager App SQL Server Express
OutputBaseFilename=Production_Manager_App_Installer_v1.0.0
OutputDir=installer_build
SetupIconFile=photo.ico
Compression=lzma
SolidCompression=yes
LicenseFile=InstallerPayload\LICENSE.txt
PrivilegesRequired=admin

[Code]

var
  DBPage: TWizardPage;
  LabelDB: TNewStaticText;
  RB_SQLExpress: TNewRadioButton;
  RB_SQLServer: TNewRadioButton;
  UseSQLExpress: Boolean;

procedure InitializeWizard;
begin
  DBPage := CreateCustomPage(
    wpLicense,
    'Database Selection',
    'Choose which database this application will use.'
  );

  LabelDB := TNewStaticText.Create(DBPage);
  LabelDB.Parent := DBPage.Surface;
  LabelDB.Caption := 'Select the database type you plan to use:';
  LabelDB.Top := ScaleY(8);
  LabelDB.Left := ScaleX(8);

  RB_SQLExpress := TNewRadioButton.Create(DBPage);
  RB_SQLExpress.Parent := DBPage.Surface;
  RB_SQLExpress.Caption := 'SQL Express (recommended for small companies)';
  RB_SQLExpress.Checked := True;
  RB_SQLExpress.Top := LabelDB.Top + ScaleY(24);
  RB_SQLExpress.Left := ScaleX(16);

  RB_SQLServer := TNewRadioButton.Create(DBPage);
  RB_SQLServer.Parent := DBPage.Surface;
  RB_SQLServer.Caption := 'SQL Server (for companies with a dedicated server)';
  RB_SQLServer.Top := RB_SQLExpress.Top + ScaleY(24);
  RB_SQLServer.Left := ScaleX(16);
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;

  if CurPageID = DBPage.ID then
  begin
    if RB_SQLExpress.Checked then
      UseSQLExpress := True
    else
      UseSQLExpress := False;
  end;
end;

function GetDBFlag(Param: string): string;
begin
  if UseSQLExpress then
    Result := '1'
  else
    Result := '0';
end;

function IsSQLExpressSelected: Boolean;
begin
  Result := UseSQLExpress;
end;

[Files]
Source: "InstallerPayload\Production Manager App.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "InstallerPayload\README.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "InstallerPayload\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "InstallerPayload\photo.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "InstallerPayload\SQLEXPRESS_EXTRACTED\*"; DestDir: "{tmp}\SQLEXPRESS_EXTRACTED"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Production Manager App"; Filename: "{app}\Production Manager App.exe"; IconFilename: "{app}\photo.ico"
Name: "{commondesktop}\Production Manager App"; Filename: "{app}\Production Manager App.exe"; IconFilename: "{app}\photo.ico"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Run]

; Install SQL Express ONLY if selected
Filename: "{tmp}\SQLEXPRESS_EXTRACTED\setup.exe"; \
    Parameters: "/QS /ACTION=Install /FEATURES=SQLEngine /INSTANCENAME=SQLEXPRESS /TCPENABLED=1 /NPENABLED=1 /IACCEPTSQLSERVERLICENSETERMS"; \
    Flags: waituntilterminated; \
    Check: IsSQLExpressSelected

; Enable TCP/IP ONLY if SQL Express was installed
Filename: "reg.exe"; \
    Parameters: "add ""HKLM\SOFTWARE\Microsoft\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQLServer\SuperSocketNetLib\Tcp"" /v Enabled /t REG_DWORD /d 1 /f"; \
    Flags: runhidden waituntilterminated; \
    Check: IsSQLExpressSelected

; Enable Named Pipes ONLY if SQL Express was installed
Filename: "reg.exe"; \
    Parameters: "add ""HKLM\SOFTWARE\Microsoft\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQLServer\SuperSocketNetLib\Np"" /v Enabled /t REG_DWORD /d 1 /f"; \
    Flags: runhidden waituntilterminated; \
    Check: IsSQLExpressSelected

; Restart SQL Express service ONLY if installed
Filename: "sc.exe"; Parameters: "stop MSSQL$SQLEXPRESS"; Flags: runhidden waituntilterminated; Check: IsSQLExpressSelected
Filename: "sc.exe"; Parameters: "start MSSQL$SQLEXPRESS"; Flags: runhidden waituntilterminated; Check: IsSQLExpressSelected

; Launch app
Filename: "{app}\Production Manager App.exe"; Flags: nowait postinstall skipifsilent
Filename: "{app}\README.txt"; Flags: postinstall shellexec skipifsilent

[Registry]
Root: HKLM; Subkey: "Software\ProductionManagerApp"; ValueType: string; ValueName: "UseSQLExpress"; ValueData: "{code:GetDBFlag}"