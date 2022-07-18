# Qapharnaum
Simple note-taking software

[Download stable version](https://github.com/SultanRancho/Qapharnaum/raw/main/note.exe)
# Illustration
![This is an image](screenshot.jpg)

# Tips
Create a Windows shortcut and associate it to a keyboard shortcut for start with keyboard.

# For dev
Require:
```shell
  pip install PyQt5
  pip install keyboard
  pip install functools
```
Build from source :
Using [pyinstaller](https://pypi.org/project/pyinstaller/)
```shell
  pip install pyinstaller
  pyinstaller note.py --onefile --noconsole --icon=icon.ico
```
