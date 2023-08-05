FROM python:3.7.9-slim

RUN pip install poetry

RUN apt-get update && \
    apt-get install -y make git build-essential && \
    apt-get clean

COPY ./containers/base/.secrets/id_rsa /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa
RUN ssh-keyscan -H gitlab.com >> /root/.ssh/known_hosts

COPY ./python/poetry.lock /app/
COPY ./python/pyproject.toml /app/
COPY ./python/Makefile /app/

WORKDIR /app/

RUN make setup-env-common

COPY ./containers/base/entrypoint.sh /root/entrypoint.sh

RUN chmod o+x /root/entrypoint.sh

ENTRYPOINT ["/root/entrypoint.sh"]

CMD ["python"]
