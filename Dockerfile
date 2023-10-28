FROM python:3.7.16-slim-buster

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install --no-install-recommends -y vim && \
    # Delete packaging metadata and cache
	rm -rfv /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

EXPOSE 8080

COPY . /usr/src/app/

RUN chmod +x entrypoint.sh
CMD ["/usr/src/app/entrypoint.sh"]
