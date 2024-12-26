## Project structures

**services** : contains all different services
**gps_producer** : contain the script to send GPS coordinate to kafka brokers

in **services** : 

**database/init.sql** : the init script of the postgresql db

## Run the app

Create a .env file in the services repository with the key BROKER_IP=your_ip_adress

launch the docker compose file : `docker compose build` and `docker compose up`

launch the gps generator in gps_producer/generate.py with args 


## URLS:

localhost:1234 : the web ui 
localhost:8080 : pgAdmin ui # user : admin@admin.fr password : admin
localhost:8888 : kafka ui