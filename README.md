# Cloud Connector
Simple cloud connector to send data to Adafruit IO.

## Docker
```
docker build . -t cloud-connector  
``` 
```
docker run -v <directory_path_of_config.json>:/config --network=host cloud-connector 
``` 

