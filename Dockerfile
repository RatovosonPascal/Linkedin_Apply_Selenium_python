# Utiliser une image de base Python
FROM python:3.9-slim

# Installer les dépendances système nécessaires pour Selenium, Chrome, curl et unzip
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Télécharger et installer ChromeDriver
RUN wget --tries=3 -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.35/linux64/chromedriver-linux64.zip && \
    echo "Téléchargement terminé, décompression maintenant..." && \
    unzip /tmp/chromedriver.zip -d /tmp/ && \
    echo "Décompression terminée, suppression du fichier temporaire..." && \
    rm /tmp/chromedriver.zip && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    echo "Installation de Chromedriver terminée."

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires dans le container
COPY requirements.txt .
COPY main.py .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut pour exécuter le script
CMD ["python", "main.py"]
