FROM python:3.7

ENV CLI_CLIENT_USER "automatic-client"
ENV CLI_CLIENT_PASSWORD "noonewilleverguess3"
ENV DATA_ENDPOINT "http://localhost:5000/gateway-with-auth/"
ENV AUTH_ENDPOINT "http://localhost:7000/"
ENV USERNAME "enduser"
ENV PASSWORD "password"
ENV DELAY 2
ENV METRICS "cpu"

ADD . /cli_client/
RUN pip install /cli_client/
CMD python "/cli_client/main.py" -e "${DATA_ENDPOINT}" -a "${AUTH_ENDPOINT}" -u "${USERNAME}" -p "${PASSWORD}" -d "${DELAY}" -m ${METRICS}
