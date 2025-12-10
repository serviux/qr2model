# Dockerfile
FROM python:3.13-slim
WORKDIR  /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["fastapi", "run", "app/app.py", "--port", "80"]
