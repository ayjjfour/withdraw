#/bin/bash

pyuic4 -o ./ui/uiframe.ui ./ui/uiframe.py
pyinstaller -F -w --distpath ./run --workpath ./run/build main.py
cp ./run/main.exe d:/withdraw/main.exe
