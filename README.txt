Wymagania:
- Python 3.12.1 (Program powinien działać na poprzednich wersjach Pythona 3)
- Biblioteki: pygame, math, sys, socket, threading, queue, random
Wszystkie biblioteki poza pygame należą do biblioteki standardowej pythona. W celu zainstalowania pygame, należy użyć komendy:
pip install pygame


Uruchamianie:
W plikach SETTINGS.py zarówno w katalogu Server oraz Client należy zmienić adres ip oraz port (Podstawowo jest to "127.0.0.1:12345").

Następnie należy uruchomić plik Server/main.py:
cd Server
python main.py

I dowolną liczbę razy uruchomić plik Client/main.py:
cd Client
python main.py