@echo off

set SCRIPTS_DIR=%0\..\



python "%SCRIPTS_DIR%/export.py" --platform=windows --arch=x86 --config=debug
python "%SCRIPTS_DIR%/export.py" --platform=windows --arch=x86_64 --config=debug



python "%SCRIPTS_DIR%/export.py" --platform=windows --arch=x86 --config=release
python "%SCRIPTS_DIR%/export.py" --platform=windows --arch=x86_64 --config=release