Copy and configure env's:
```bash
cp ./app/.env.example ./app/.env
```
Create network
```bash
docker network create noticer
```
Build and run project:
```bash
docker compose up -d
```