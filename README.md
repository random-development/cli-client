# cli-client
Program automatycznie przeszukujący monitorowane zasoby i pomiary w celu wyświetlenia (co pewien czas odświeżonych wyników dla) top 10 najbardziej obciążonych maszyn.


# Możliwości cli-client
- dostęp do API gateway oparty na mikrousłudze uwierzytelniającej [FIXME: gatharing data task]
- może podłączyć się do kilku onitorów jednocześnie [FIXME: gatharing data task]
- uwzględnia zmiany (wykrywa dodanie nowych lub usunięcie istniejących maszyn z listy monitorowanych zasobów) [FIXME: gatharing data task]
- wypisuje i co pewien czas odświeża top 10 najbardziej obciążonych maszyn [FIXME: printing data task]

# Instalacja i uruchomienie cli-client

## Uruchomnienie aplikacji w kontenerze

Checkout źródeł
```bash
git clone git@github.com:random-development/cli-client.git
```

Zbudowanie obrazu
```bash
cd cli-client
sudo docker build -t python-cli-client .
```

Uruchomienie kontenera
```bash
sudo docker run -e ENDPOINT="<endpoint_url>" -e USERNAME="<username>" -e PASSWORD="<password>" python-cli-client
```

## Uruchomnienie aplikacji manualne

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
```bash
./main.py --endpoint "<endpoint_url>" --username "<username>" --password "<password>" 
```

# Testy jednostkowe

## Uruchomienie testów w kontenerze

Checkout źródeł
```bash
git clone git@github.com:random-development/cli-client.git
```

Zbudowanie obrazu
```bash
cd cli-client
sudo docker build -t python-cli-client-test -f Dockerfile.test .
```

Uruchomienie kontenera
```bash
sudo docker run python-cli-client-test
```

## Uruchomienie testów manualne
```bash
git clone git@github.com:random-development/cli-client.git
cd cli-client
python -m pytest tests/
```

[FIXME: gatharing data task]: https://github.com/random-development/resources-monitoring-system/issues/40
[FIXME: printing data task]: https://github.com/random-development/resources-monitoring-system/issues/39
