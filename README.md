# HackCulture2018
This app was designed as part of HackCulture 2018 (https://publish.illinois.edu/hackculture/)

We designed this app to map out the safest route (instead of the shortest ones provided by Google Maps).

Routes are determined by crime data obtained from the City of Urbana (https://data.urbanaillinois.us/Police/Police-Incidents-Since-1988/uj4k-8xe8)

Each incidence of crime is given a weightage depending on the recency of the crime. A total score is then calculated, and the route with the lowest score will be selected.

## Setup
-Python 2.7

-Flask:
``` pip install Flask ```

-Jinja:
``` pip install Jinja2 ```

-Flask-GoogleMaps:
```bash
git clone https://github.com/rochacbruno/Flask-GoogleMaps
cd Flask-GoogleMaps
python setup.py install
```

## How to run
In command line, type:

```FLASK_APP=main.py flask run```
or
```python main.py```

Then, go to http://localhost:5000/

Type in the start and end destinations and you will get the safest route!
