# GPS Plane Tracker

This project is a GPS tracker for airplanes. It was built using various technologies to implement a microservices architecture, with Kafka, FastAPI, PostgreSQL, Vue, and Docker.


## Project structures

**services** : contains all different services


**gps_producer** : contain the script to send GPS coordinate to kafka brokers

#### In the **services** repository: 

**database/init.sql** : the init script of the postgresql db

**.env** : the code for environnements variables


**docker-compose.yml** : the docker compose file to launch the project

## Run the app

Create a .env file in the **services** repository with the key `BROKER_IP=your_ip_adress` 

launch the docker compose file : `docker compose build` and `docker compose up`

Next wait few seconds and go to the web ui at `http://localhost:1234/` 

To launch a plane first go in **gps_producer** repository , next edit the environnements variables of the docker file to add the key `BROKER_IP=your_ip_adress` 
Build the docker image with this command : `docker build -t gps_producer .`

Next start a plane by launching this command : 

`docker run gps_producer --plane_id="YourPlaneID" --start_city="YourStartCity" --end_city="YourEndCity"`

Exemple : 

`docker run gps_producer --plane_id="A307_14" --start_city="Paris" --end_city="Madrid"`

Go on the web UI and you will see the plane data
 

 


## URLS:

localhost:1234 : the web ui 


localhost:8080 : pgAdmin ui # user : admin@admin.fr password : admin


localhost:8888 : kafka ui