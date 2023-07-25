FROM python:3.8

RUN mkdir /opt/fetch
WORKDIR /opt/fetch
COPY . .

RUN python3 -m venv .venv && \
    source .venv/bin/activate && \
    python3 -m pip install -r requirements.txt




CMD ["python3","-m","flask","run","--host=0.0.0.0","--port=5000"]