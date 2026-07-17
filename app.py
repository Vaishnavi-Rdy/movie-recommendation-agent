from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

movies = []

with open("movies.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        if not row["Movie"] or not row["Genre"]:
            continue

        row["Movie"] = row["Movie"].strip()
        row["Genre"] = row["Genre"].strip()

        poster_name = row["Movie"].lower().replace(" ", "") + ".jpg"

        poster_path = os.path.join(app.static_folder, "posters", poster_name)

        if os.path.exists(poster_path):
            row["Poster"] = poster_name
        else:
            row["Poster"] = "default.jpg"

        movies.append(row)


@app.route("/")
def home():
    genres = sorted(list(set(movie["Genre"] for movie in movies)))
    return render_template("index.html", genres=genres)


@app.route("/recommend", methods=["POST"])
def recommend():
    genre = request.form["genre"].strip()

    recommendations = []

    for movie in movies:
        if movie["Genre"].strip().lower() == genre.lower():
            recommendations.append(movie)

    recommendations.sort(
        key=lambda x: float(x["Rating"]),
        reverse=True
    )

    return render_template(
        "result.html",
        genre=genre,
        movies=recommendations
    )


if __name__ == "__main__":
    app.run(debug=False)