FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update; apt install -y python3-pip ffmpeg; apt clean

WORKDIR /app

COPY requirements.txt /app

RUN python3 -m pip install -r requirements.txt

COPY . /app

EXPOSE 8000

ENTRYPOINT ["python3"]

CMD ["app.py"]