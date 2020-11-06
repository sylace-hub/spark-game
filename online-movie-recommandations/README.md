# On-line recommendation service.

The CherryPy framework features a reliable, HTTP/1.1-compliant, WSGI thread-pooled webserver.
```console
pip3 install CherryPy
```

Flask is a micro web framework written in Python.
```console
pip3 install Flask
```

**Our complete web service contains three Python files:**
* engine.py defines the recommendation engine, wrapping inside all the Spark related computations.
* app.py is a Flask web application that defines a RESTful-like API around the engine.
* server.py initialises a CherryPy webserver after creating a Spark context and Flask web app using the previous.

To run the server :
```console
$ python server.py ml-latest/movies.csv ml-latest/ratings.csv
```

## The application deploys three rest services :

### Getting Top Recommendations :

Here we call the service to get the top 10 recommendations for the user 331 :
```console
$ curl -H "Accept: application/json; Content-Type: application/json" -X GET http://localhost:5432/331/ratings/top/10 | python -m json.tool
```

### Getting Individual Ratings :

Here we call the to get the predicted rating for the movie The Quiz (1994) for the user 12 :
```console
$ curl -H "Content-Type: application/json" -X GET http://localhost:5432/12/ratings/858
```

### Adding New Ratings

Add new ratings for a specific user and recompute the prediction model for every new batch of user ratings.
Here we call the service for the user 331 :
```console
$ curl -H "Accept: text/csv; Content-Type: application/json" -X POST http://localhost:5432/331/ratings -F 'file=@ml-latest/new-ratings.csv'
```

The format is a series of lines (ending with the newline separator) with movie_id and rating separated by commas. For example, the following file corresponds to the ten new user ratings used as a example in the tutorial about building the model:
```csv
260,4.6  
1,4
16,3.5  
25,4  
32,5 
335,4
379,3
296,1
858,1
50,2.3
```
