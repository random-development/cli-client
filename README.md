# cli-client [![Build Status](https://travis-ci.org/random-development/cli-client.svg?branch=master)](https://travis-ci.org/random-development/cli-client)
Program automatycznie przeszukujący monitorowane zasoby i pomiary w celu wyświetlenia (co pewien czas odświeżonych wyników dla) top 10 najbardziej obciążonych maszyn.

# Możliwości cli-client
- Dostęp do API gateway oparty na mikrousłudze uwierzytelniającej.
- Może podłączyć się do kilku monitorów jednocześnie (za pomocą resource `/metrics` API Gateway); przy tym uwzględnia zmiany (wykrywa dodanie nowych lub usunięcie istniejących maszyn z listy monitorowanych zasobów).
- Wypisuje i co pewien czas (ok. 1 min.) odświeża top 10 najbardziej obciążonych maszyn.

# Instalacja i uruchomienie cli-client

## Opis parametrów
```bash
$ ./main.py --help
usage: main.py [-h] -e DATA_ENDPOINT -a AUTH_ENDPOINT -u USERNAME -p PASSWORD               [-d DELAY] [-m METRICS [METRICS ...]]

CLI for monitoring resources.

optional arguments:
  -h, --help            show this help message and exit
  -e DATA_ENDPOINT, --data-endpoint DATA_ENDPOINT
                        Enpoint for gathering monitoring data.
  -a AUTH_ENDPOINT, --auth-endpoint AUTH_ENDPOINT
                        Enpoint for authentication microservice.
  -u USERNAME, --username USERNAME
                        Username for API Gateway authentication.
  -p PASSWORD, --password PASSWORD
                        Password for API Gateway authentication.
  -d DELAY, --delay DELAY
                        Delay time (default 2 sec).
  -m METRICS [METRICS ...], --metrics METRICS [METRICS ...]
                        Metrics to show - space separated list. First element
                        defines key for sorting to display top resources
                        (default cpu).
```

Dodatkowo warto pamiętać, że:
- `DELAY` - jest parametrem periodycznego odświeżania dashboadu (tabeli), natomiast pobieranie dzieje się w osobnej korutynie w pętli.
- `METRICS` - pierwsza metryka w liście jest parametrem sortowania "top"
- `USERNAME`, `PASSOWRD` - stanowią dane użytkownika

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

Uruchomienie kontenera z domyslnymi parametrami
```bash
sudo docker run -it python-cli-client
```

Uruchomienie kontenera ze zmienionymi parametrami (należy pamiętać o podaniu końcowych znaków `/` w przypadku definiowania endpointów)
```bash
sudo docker run -it -e CLI_CLIENT_USER="<cli_client_user>" -e CLI_CLIENT_PASSWORD="<cli+client_password>" -e DATA_ENDPOINT="<data_endpoint_url>" -e AUTH_ENDPOINT="<auth_endpoint_url>" -e USERNAME="<username>" -e PASSWORD="<password>" -e DELAY=10 -e METRICS="<metrics_list>" python-cli-client
```

Przykładowe uruchomienie ze zmienionymi parametrami
```bash
sudo docker run -it -e CLI_CLIENT_USER="automatic-client" -e CLI_CLIENT_PASSWORD="noonewilleverguess3" -e DATA_ENDPOINT="http://hibron.usermd.net:5000/gateway-with-auth/" -e AUTH_ENDPOINT="http://hibron.usermd.net:7000/" -e USERNAME="enduser" -e PASSWORD="password" -e DELAY=10 -e METRICS="metricName0 metricName1" python-cli-client
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

Uruchomienie narzędzia (tu oprócz parametrów należy pamiętać o ustawieniu zmiennych `CLI_CLIENT_USER` oraz `CLI_CLIENT_PASSWORD` do autoryzacji aplikacji)
```bash
./main.py --data-endpoint "<data_endpoint_url>" --auth-endpoint "<auth_endpoint_url>" --username "<username>" --password "<password>" --delay 3 -m temp mem # delay time and metrics are optional
```

Przykladowe użycie
```bash
CLI_CLIENT_USER=automatic-client CLI_CLIENT_PASSWORD=noonewilleverguess3 ./main.py  -e "http://hibron.usermd.net:5000/gateway-with-auth/" -a "http://hibron.usermd.net:7000/" -u enduser -p password -d 1 -m metricName0 metricName1
```

# Widok dashboardu

Przy oczekiwaniu na dane
![init dashboard](https://i.imgur.com/0oYCyv5.png "Init dashboard")

Po pobraniu danych (ok. 1 min) top 10 dla metryki `metricName0`
![data dashboard](https://imgur.com/3NG7iFo.png "Data dashboard")

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
