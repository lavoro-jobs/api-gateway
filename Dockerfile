FROM python:3.9-alpine AS base

WORKDIR /app

FROM base AS development

COPY ./lavoro-api-gateway/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN apk add curl bash

RUN curl -sS https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -o /wait-for-it.sh \
    && chmod +x /wait-for-it.sh

COPY ./lavoro-library/pre_install.sh /app/pre_install.sh
RUN chmod +x /app/pre_install.sh
RUN /app/pre_install.sh

COPY ./lavoro-library/lavoro_library /app/lavoro_library
COPY ./lavoro-api-gateway/lavoro_api_gateway /app/lavoro_api_gateway

ENV PYTHONPATH "${PYTHONPATH}:/app"

ENTRYPOINT ["/wait-for-it.sh", "pgsql:5432", "--timeout=150", "--"]
CMD ["uvicorn", "lavoro_api_gateway.api_gateway:app", "--host", "0.0.0.0", "--port", "80"]

FROM base AS production

COPY ./requirements-prod.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./lavoro_api_gateway /app/lavoro_api_gateway

ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN pip install gunicorn

CMD ["gunicorn", "lavoro_api_gateway.api_gateway:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:80"]