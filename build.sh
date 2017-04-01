#/bin/bash

pyinstaller -F -w --distpath ./run --workpath ./run/build main.py
cp ./run/main.exe d:/withdraw/main.exe
