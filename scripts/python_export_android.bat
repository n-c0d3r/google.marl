@echo off

set SCRIPTS_DIR=%0\..\



python "%SCRIPTS_DIR%/export.py" --platform=android --arch=x86 --config=debug
python "%SCRIPTS_DIR%/export.py" --platform=android --arch=x86_64 --config=debug
python "%SCRIPTS_DIR%/export.py" --platform=android --arch=arm64-v8a --config=debug
python "%SCRIPTS_DIR%/export.py" --platform=android --arch=armeabi-v7a --config=debug



python "%SCRIPTS_DIR%/export.py" --platform=android --arch=x86 --config=release
python "%SCRIPTS_DIR%/export.py" --platform=android --arch=x86_64 --config=release
python "%SCRIPTS_DIR%/export.py" --platform=android --arch=arm64-v8a --config=release
python "%SCRIPTS_DIR%/export.py" --platform=android --arch=armeabi-v7a --config=release