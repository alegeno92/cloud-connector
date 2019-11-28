FROM python:3-alpine
RUN pip install --no-cache-dir paho-mqtt adafruit-io
RUN mkdir /app
WORKDIR /app
COPY *.py /app/
CMD ["python", "-u", "/app/main.py" , "/config/config.json"]
