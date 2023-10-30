FROM python:3.9

WORKDIR /devel

COPY ./requirements.txt /devel/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /devel/requirements.txt

COPY ./lavoro_api_gateway /devel/lavoro_api_gateway

CMD ["uvicorn", "lavoro_api_gateway.api_gateway:app", "--host", "0.0.0.0", "--port", "80"]
