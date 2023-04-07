# How to uruchomić backend

## 1. Sklonować projekt

## 2. Wejść do katalogu projektu

## 3. Stworzyć środowisko wirtualne

trzeba napisać w konsoli: **python3 -m venv venv**\
lub: **python -m venv venv** jesli nie masz python3

## 4. Uruchomić środowisko wirtualne

trzeba napisać w konsoli:

- MacOS: **source venv/bin/activate**
- windows: **source venv/Scripts/activate**
- Linux: **source venv/???/activate**, nie wiem, nie sprawdzałem

## 5. Sprawdzić czy się uruchomiło

trzeba napisać w konsoli: **which python**\
powninno to wyświetlić ścieżkę do pythona w środowisku wirtualnym

## 6. Zainstalować kilka pakietów

trzeba napisać w konsoli: **pip install -r requirements.txt**

## 7. Uruchomić program kiedy znajdujesz się w katalogu projektu

1. trzeba wejsć do katalogu **app**
2. trzeba napisać w konsoli: **uvicorn main:app --port 8000 --reload**

ta komenda uruchomi program na porcie 8000, **nie trzeba tego zmieniać**, ten port jest zahardkodowany na frontendzie
