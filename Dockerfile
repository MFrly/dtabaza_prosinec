# Použití základního obrazu Python
FROM python:3.9-slim

# Nastavení pracovního adresáře
WORKDIR /app

# Kopírování požadavků a aplikace do kontejneru
COPY requirements.txt ./
COPY . .

# Instalace požadavků Pythonu
RUN pip install --no-cache-dir -r requirements.txt

# Exponování portu, na kterém Flask aplikace běží
EXPOSE 5000

# Příkaz pro spuštění aplikace
CMD ["python", "app.py"]
