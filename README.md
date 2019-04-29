# cli-client
Program automatycznie przeszukujący monitorowane zasoby i pomiary w celu wyświetlenia (co pewien czas odświeżonych wyników dla) top 10 najbardziej obciążonych maszyn.


# Możliwości cli-client
- dostęp do API gateway oparty na mikrousłudze uwierzytelniającej [FIXME: gatharing data task]
- może podłączyć się do kilku onitorów jednocześnie [FIXME: gatharing data task]
- uwzględnia zmiany (wykrywa dodanie nowych lub usunięcie istniejących maszyn z listy monitorowanych zasobów) [FIXME: gatharing data task]
- wypisuje i co pewien czas odświeża top 10 najbardziej obciążonych maszyn [FIXME: printing data task]

# Instalacja i uruchomienie cli-client

## Instalacja manualna

Checkout źródeł
```bash
git clone git@github.com:random-development/cli-client.git
```

Zbudowanie projektu
```bash
cd cli-client
pip install .
```

Uruchomienie narzędzia
```
./main.py
```

[FIXME: gatharing data task]: https://github.com/random-development/resources-monitoring-system/issues/40
[FIXME: printing data task]: https://github.com/random-development/resources-monitoring-system/issues/39
