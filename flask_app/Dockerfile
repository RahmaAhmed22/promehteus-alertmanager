FROM python:3.15.0a6-slim
WORKDIR /app
RUN pip3 install flask prometheus-client
COPY app.py .
CMD ["python3", "app.py"]