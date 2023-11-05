FROM python:3.9

WORKDIR /devel

COPY ./lavoro-api-gateway/requirements.txt /devel/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /devel/requirements.txt

COPY ./lavoro-api-gateway/lavoro_api_gateway /devel/lavoro_api_gateway


# Library 
COPY ./lavoro-library/lavoro_library /devel/lavoro_library
COPY ./lavoro-library/pre_install.sh /devel/pre_install.sh

RUN chmod +x /devel/pre_install.sh
RUN /devel/pre_install.sh

ENV PYTHONPATH "${PYTHONPATH}:/devel"

CMD ["uvicorn", "lavoro_api_gateway.api_gateway:app", "--host", "0.0.0.0", "--port", "80"]