FROM python:3.9.10-alpine3.14
WORKDIR /srv
RUN pip install --upgrade pip
RUN pip install flask
RUN pip install flask_oidc
COPY ./src /srv
ENV FLASK_APP=app
CMD ["python","app.py"]