FROM python:3.12.6-slim-bullseye

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "main.py"]