# Habr Proxy reader

Does nothing useful, just adds a trademark symbol to every 6-character word. 

### Features

* All Harb links are processed as local
* SVG is supported
* Formulas are supported

### Limitations

* Some ads may not work correctly (probaly due to the domain limitations)
* Unstable while working with bad connection
* Kinda slow

### Using with docker

To run the server in container:

```bash
docker build -t habr-proxy . && docker run -i -t -p 8018:8018 habr-proxy
```

Then go to [localhost:8018](http://localhost:8018/)

### Using without docker 

Just install dependencies from requirements.txt and run main.py (use -h flag to see help):

```bash
python main.py
```

It may be a little different depending on your system. Using virtual enviroment is recommended.