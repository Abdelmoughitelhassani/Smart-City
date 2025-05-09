
# Smart City IoT Streaming Pipeline  

## Description  
**Smart City IoT Streaming Pipeline** est un pipeline de traitement de données en temps réel simulant une ville intelligente. Il permet de générer, ingérer, traiter et stocker des flux de données provenant de capteurs IoT simulés liés aux véhicules, au trafic routier, aux conditions météorologiques et aux incidents d’urgence. Le projet utilise les technologies Big Data suivantes :  
- **Apache Kafka** pour l’ingestion des flux de données  
- **Apache Spark Structured Streaming** pour le traitement en continu  
- **Apache Cassandra** pour le stockage des résultats  
- **Docker** pour l’orchestration des services  
- **PySpark** et **Python** pour le développement des producteurs et traitements  

## Architecture  

```
[ Python Producer ] ---> [ Kafka Topics ] ---> [ Spark Streaming ] ---> [ Cassandra DB ]
        ↑                                                   ↓
  Données simulées                                  Traitement temps réel
 (GPS, trafic, météo, urgences)
```

## Types de données simulées  

- **GPS** : latitude, longitude, vitesse, direction  
- **Trafic** : ID de caméra, position, images  
- **Météo** : température, humidité, AQI, vent  
- **Urgences** : feu, accident, médical, police  
- **Véhicule** : modèle, année, type de carburant  

## Installation et Exécution  

```bash
# Cloner le projet
git clone https://github.com/Abdelmoughitelhassani/Smart-City.git
cd Smart-City

# Construire l’image du producteur Kafka
cd jobs
docker build -t kafka-producer .
cd ..

# Lancer les services
docker-compose up -d

# Lancer le job Spark
docker exec -it spark-master spark-submit \
  --master spark://spark-master:7077 \
  --conf spark.sql.streaming.kafka.bootstrap.servers=kafka:9092 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2,com.datastax.spark:spark-cassandra-connector_2.12:3.3.0,com.github.jnr:jnr-posix:3.1.15 \
  /opt/bitnami/spark/jobs/smartcity.py
```
