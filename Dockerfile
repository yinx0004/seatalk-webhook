FROM ubuntu:20.04

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

ENV DEBIAN_FRONTEND=noninteractive TZ=Asia/Singapore

RUN apt-get update && apt-get install -y tzdata python3.9 python3-pip && pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
