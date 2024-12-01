# Instalacja środowiska wirtualnego
Jeżeli w nazwię folderu występują spację, należy taką nazwę napisać w cudzysłowie

**Windows (cmd)**
```
python3 -m venv .venv
.venv\Scripts\activate.bat
python3 -m pip install -r <path to project\requirements.txt>
```

**Unix/macOS (bash/zsh)**
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r <path to project/requirements.txt>
```

# Uruchamianie programu
```
python3 Scraper <webpage> <path to thumbnails folder> <path to logos folder> <path to images folder> <path to folder with JSON files>
```
lub z poziomu projektu
```
python3 __main__.py <webpage> <path to thumbnails folder> <path to logos folder> <path to images folder> <path to folder with JSON files>
```

# Deaktywacja środowiska wirtualnego
```
deactivate
```