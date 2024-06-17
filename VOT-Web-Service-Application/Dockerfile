FROM python:3.9.10-alpine3.14
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install flask
RUN pip install flask_oidc
RUN pip install flask_cors
COPY . /app
ENV FLASK_APP=app
EXPOSE 5000
CMD ["python","app.py"]