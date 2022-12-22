FROM python:3.10

COPY . /root/
WORKDIR /root/

RUN apt-get update
RUN apt-get install -y ffmpeg

RUN pip3 install -U pip
RUN pip3 install -U -r requirements.txt

CMD ["python3", "-m", "FidoSelf"]
