FROM python:3.11.3-slim-buster as build

ENV PYTHONUNBUFFERED=1

WORKDIR /app
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

FROM python:3.11.3-slim-buster
WORKDIR /app
COPY --from=build /app/venv ./venv
COPY ./kernel_api/requirements.txt .
RUN pip install -r requirements.txt

COPY ./kernel_api/db ./db
COPY ./kernel_api/main.py .
COPY ./kernel_api/configs ./configs
COPY ./kernel_api/routers ./routers
COPY ./kernel_api/middleware ./middleware
COPY ./kernel_api/dependencies ./dependencies
COPY ./kernel_api/base_classes ./base_classes
COPY ./kernel_api/deploy_serv/uvicorn_settings.py .
COPY ./kernel_api/deploy_serv/entrypoint.sh ./deploy_serv/entrypoint.sh
RUN chmod +x ./deploy_serv/entrypoint.sh
ENTRYPOINT ["./deploy_serv/entrypoint.sh"]
