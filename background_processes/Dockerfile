FROM python:3.11.3-slim-buster as build

ENV PYTHONUNBUFFERED=1

WORKDIR /app
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

FROM python:3.11.3-slim-buster
WORKDIR /app
COPY --from=build /app/venv ./venv

COPY ./background_processes/requirements.txt .
RUN pip install -r ./requirements.txt

COPY ./background_processes/main.py .
COPY ./background_processes/entrypoint.sh .
COPY ./background_processes/configs ./configs
COPY ./background_processes/db ./db
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
