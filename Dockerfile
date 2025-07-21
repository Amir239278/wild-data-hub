FROM python:3.10-slim

# 📂 Création des dossiers
WORKDIR /app
RUN mkdir /app/dataset

# 📦 Installation des dépendances
COPY requirements_cron.txt ./
RUN pip install --no-cache-dir -r requirements_cron.txt


# 📝 Ajout du script et de la crontab
COPY collecte_dvf.py crontab.txt ./

# ⏱️ Ajout crontab au système
RUN apt-get update && apt-get install -y cron \
  && crontab crontab.txt

# 🧼 Démarrage du cron
CMD cron -f

