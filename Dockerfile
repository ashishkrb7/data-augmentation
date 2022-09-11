FROM python:3
LABEL maintainer="Ashish Kumar <ashishkrb7@gmail.com>"
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt-get update
RUN apt-get install -y python3-opencv
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
ENTRYPOINT ["/bin/sh", "./run.sh"]
