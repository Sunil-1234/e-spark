FROM ubuntu:20.04
WORKDIR /app
RUN apt update
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y python3-pip
ADD ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt
COPY . /app
EXPOSE 5000
# ENTRYPOINT [ "waitress-serve" ]
# CMD [ "--host=0.0.0.0 --port=5000 main:app" ]
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "main:app"]