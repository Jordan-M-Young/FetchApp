# FetchApp

Name entity / key quantity extraction from emails


## Run - Locally 

to set up the project:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

To run the app:

```bash
python3 -m flask run --host=0.0.0.0 --port=5000
```


## Run Docker

### Build Image

```bash
docker build -t fetch-app .
```

### Run Container

```
docker run -p 5000:5000 fetch-app 
```


## Use app

To hit the email processing endpoint:

```
curl -X POST http://0.0.0.0:5000/process -H "Content-Type: application/json" -d '{"filename":"dummy_order.html"}'
```

* "filename" can also be changed to "dummy_shipping.html"



To check if the email database has been populated with extracted information:

```
curl -X POST http://0.0.0.0:5000/check -H "Content-Type: application/json" -d '{"filename":"dummy_order.html"}'
```