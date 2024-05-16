FROM python:3.11.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt -q
COPY . .
CMD ["chainlit", "run", "app.py", "--host","0.0.0.0", "--port", "8000"]