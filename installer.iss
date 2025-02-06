[Setup]
AppName=XML Translator
AppVersion=1.0
WizardStyle=modern
DefaultDirName={autopf}\XML Translator
DefaultGroupName=XML Translator
UninstallDisplayIcon={app}\XML Translator.exe
Compression=lzma2
SolidCompression=yes
OutputDir=Output
OutputBaseFilename=XML_Translator_Setup

[Files]
Source: "dist\XML Translator\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\XML Translator"; Filename: "{app}\XML Translator.exe"
Name: "{commondesktop}\XML Translator"; Filename: "{app}\XML Translator.exe" 