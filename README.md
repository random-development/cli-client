# cli-client [![Build Status](https://travis-ci.org/random-development/cli-client.svg?branch=master)](https://travis-ci.org/random-development/cli-client)
Program automatycznie przeszukujący monitorowane zasoby i pomiary w celu wyświetlenia (co pewien czas odświeżonych wyników dla) top 10 najbardziej obciążonych maszyn.

# Możliwości cli-client
- dostęp do API gateway oparty na mikrousłudze uwierzytelniającej [FIXME: auth microservice]
- może podłączyć się do kilku monitorów jednocześnie [FIXME: gatharing data task]
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
sudo docker run -it -e ENDPOINT="<endpoint_url>" -e USERNAME="<username>" -e PASSWORD="<password>" -e DELAY=3 -e METRICS="cpu temp mem" python-cli-client
```

## Uruchomnienie aplikacji manualne

Checkout źródeł
```bash
git clone git@github.com:random-development/cli-client.git
```

Zbudowanie projektu (powinno się przed tym utworzyć [virtualenv])
```bash
cd cli-client
pip install .
```

Uruchomienie narzędzia
```bash
./main.py --endpoint "<endpoint_url>" --username "<username>" --password "<password>" --delay 3 # delay time is optional
```

# Testy jednostkowe (+ linter)

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

Powinno się przed tym utworzyć [virtualenv].

```bash
git clone git@github.com:random-development/cli-client.git
cd cli-client
python -m pytest tests/
pylint cli_client --disable=fixme
```

[FIXME: gatharing data task]: https://github.com/random-development/resources-monitoring-system/issues/40
[FIXME: printing data task]: https://github.com/random-development/resources-monitoring-system/issues/39
[FIXME: auth microservice]: https://github.com/random-development/resources-monitoring-system/issues/49
[virtualenv]: https://docs.python-guide.org/dev/virtualenvs/#basic-usage
