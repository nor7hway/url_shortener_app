FROM python:3.9
WORKDIR /url_test_app
COPY . /url_test_app
RUN pip install -r requirements.txt
EXPOSE 8000
RUN ["chmod", "+x", "./docker-entrypoint.sh"]
ENTRYPOINT ["./docker-entrypoint.sh"]