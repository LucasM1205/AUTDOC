# Basis-Image
FROM node:18

# Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere package.json und package-lock.json (falls vorhanden)
COPY package.json package-lock.json ./

# Installiere die Abhängigkeiten
RUN npm install

# Kopiere den Rest des Projekts
COPY . .

# Öffne den Port für das Frontend
EXPOSE 5173

# Starte die Entwicklungsumgebung
CMD ["npm", "run", "dev", "--", "--host"]

