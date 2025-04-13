FROM python:3.8-slim

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances
RUN set -ex; \
  	pip install --no-cache-dir -r requirements.txt

# Définir le répertoire de travail
WORKDIR /

# Copier le script de gestion d'attente et le producteur Kafka
COPY wait-for-it.sh wait-for-it.sh
COPY main.py main.py

# Donner les permissions d'exécution au script
RUN chmod +x wait-for-it.sh

# Exécuter le producteur Kafka après s'être assuré que Kafka est prêt
CMD ./wait-for-it.sh -s -t 100 $KAFKA_SERVER -- python -u main.py
