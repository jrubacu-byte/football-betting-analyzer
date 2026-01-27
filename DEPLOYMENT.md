# 🚀 Guía de Despliegue

## Despliegue en Producción

### Opción 1: Heroku

```bash
# Instalar Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Crear app
heroku create football-betting-analyzer

# Configurar variables de entorno
heroku config:set LLM_API_KEY=your_key
heroku config:set ENVIRONMENT=production

# Desplegar
git push heroku main

# Ver logs
heroku logs --tail
```

### Opción 2: AWS EC2

```bash
# Conectar a instancia
ssh -i key.pem ec2-user@your-instance-ip

# Instalar dependencias
sudo yum update -y
sudo yum install python3 python3-pip -y

# Clonar repo
git clone <repo-url>
cd football-betting-analyzer

# Instalar dependencias
pip3 install -r backend/requirements.txt

# Crear servicio systemd
sudo nano /etc/systemd/system/betting-analyzer.service
```

Contenido del servicio:
```ini
[Unit]
Description=Football Betting Analyzer
After=network.target

[Service]
Type=notify
User=ec2-user
WorkingDirectory=/home/ec2-user/football-betting-analyzer
ExecStart=/usr/local/bin/python3 -m backend.main
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Iniciar servicio
sudo systemctl start betting-analyzer
sudo systemctl enable betting-analyzer
```

### Opción 3: DigitalOcean App Platform

1. Conectar repositorio GitHub
2. Configurar variables de entorno
3. Desplegar automáticamente

## Configuración de Dominio

```bash
# Apuntar DNS a tu servidor
# A record: api.example.com → your-server-ip

# Instalar SSL con Let's Encrypt
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d api.example.com
```

## Monitoreo

```bash
# Instalar PM2 (Node.js)
npm install -g pm2

# O usar supervisor (Python)
pip install supervisor
```

## Backups

```bash
# Backup de logs
tar -czf logs-backup-$(date +%Y%m%d).tar.gz logs/

# Backup de historial (si usas DB)
pg_dump betting_analyzer > backup-$(date +%Y%m%d).sql
```
