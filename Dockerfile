FROM python:3
ADD main.py /
COPY *.py ./
RUN pip install --no-cache-dir paho-mqtt adafruit-io
CMD ["python", "./main.py" , "/config/config.json"]
