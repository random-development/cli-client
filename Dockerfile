FROM python:3.7

ENV ENDPOINT default_endpoint
ENV USERNAME default_username
ENV PASSWORD default_password
ENV DELAY 2
ENV METRICS "cpu"

ADD . /cli_client/
RUN pip install /cli_client/
CMD python "/cli_client/main.py" -e "${ENDPOINT}" -u "${USERNAME}" -p "${PASSWORD}" -d "${DELAY}" -m ${METRICS}
