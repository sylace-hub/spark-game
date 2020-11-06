from flask import Blueprint
main = Blueprint('main', __name__)
 
import json

# Find Spark
import findspark
findspark.init()

from pyspark import SparkContext
from pyspark.sql import SparkSession

from engine import RecommendationEngine

from flask import Flask, request

@main.route("/<int:user_id>/ratings", methods = ["POST"])
def add_ratings(user_id):
    print("User {} adds more ratings for movies.".format(user_id))

    uploaded_file = request.files['file']
    data = uploaded_file.read()
    ratings_list = data.decode("utf-8").strip().split("\n")
    ratings_list = map(lambda x: x.split(","), ratings_list)
    ratings = map(lambda x: (user_id, int(x[0]), float(x[1])), ratings_list)
    recommendation_engine.add_ratings(ratings)

    return "The prediction model has been recomputed for the new user ratings.\n"

@main.route("/<int:user_id>/ratings/<int:movie_id>", methods=["GET"])
def movie_ratings(user_id, movie_id):
    print("User %s rating requested for movie %s", user_id, movie_id)

    rating = recommendation_engine.predict_rating(int(user_id), int(movie_id))
    return str(rating) + "\n"

@main.route("/<int:user_id>/ratings/top/<int:count>", methods=["GET"])
def top_ratings(user_id, count):
	top_ratings = recommendation_engine.recommend_for_user(user_id, count)
	return top_ratings.toPandas().to_json(orient="records")

def create_app(spark_context, movies_set_path, ratings_set_path):
	global recommendation_engine

	recommendation_engine = RecommendationEngine(spark_context, movies_set_path, ratings_set_path)
	app = Flask(__name__)
	app.register_blueprint(main)
	return app