# Instalacja środowiska wirtualnego


**Uwaga 1.** Jeżeli w nazwie folderu występują spacje, należy taką nazwę napisać w cudzysłowie.

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

**Uwaga 1.** Ścieżki są zależne od systemu.

**Uwaga 2.** Foldery muszą być stworzone przed uruchomieniem programu.

```
python3 Scraper [<path to thumbnails folder> <path to logos folder> <path to images folder> <path to folder with JSON files>]
```

lub z poziomu projektu

```
python3 __main__.py [<path to thumbnails folder> <path to logos folder> <path to images folder> <path to folder with JSON files>]
```

Domyślne ścieżki to:
- `<path to thumbnails folder>` – `./images/thumbnails`
- `<path to logos folder>` – `./images/logos`
- `<path to images folder>` – `./images`
- `<path to folder with JSON files>` – `./results`

```
deactivate
```

# Rozpakowanie wyników scrapowania

Ze względu na limity GitHuba, rezultaty scrapowania są zapisane w ramach Git LFS w dwóch częściach. Po ściągnięciu plików należy użyć następującej komendy do utworzenia połączonego archiwum:

```
zip -s0 scrape_results.zip --out results.zip
```

Owe archiwum można potem rozpakować poprzez komendę:

```
unzip results.zip
```

Po czym wszystkie niezbędne pliki będą się znajdowały na swoim miejscu.
