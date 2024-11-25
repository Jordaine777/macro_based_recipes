from flask import Flask, render_template, request
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)

# Load the dataset
recipes_df = pd.read_csv("food_dataset/recipes.csv")

# Parse the nutrients column to extract macros if needed
if "nutrients" in recipes_df.columns:
    def parse_nutrients(nutrients_str):
        try:
            nutrients = eval(nutrients_str)
            return {
                "calories": int(nutrients.get("kcal", 0)),
                "protein": int(nutrients.get("protein", "0g").replace("g", "")),
                "carbs": int(nutrients.get("carbs", "0g").replace("g", "")),
                "fats": int(nutrients.get("fat", "0g").replace("g", "")),
            }
        except:
            return {"calories": 0, "protein": 0, "carbs": 0, "fats": 0}

    macros = recipes_df["nutrients"].apply(parse_nutrients).apply(pd.Series)
    recipes_df = pd.concat([recipes_df, macros], axis=1)

# Filter valid rows
recipes_df = recipes_df[(recipes_df["calories"] > 0) & (recipes_df["protein"] > 0)]

# Normalize macros
macro_columns = ["calories", "protein", "carbs", "fats"]
scaler = MinMaxScaler()
normalized_macros = scaler.fit_transform(recipes_df[macro_columns])

# Train the KNN model
knn = NearestNeighbors(n_neighbors=10, metric="euclidean")
knn.fit(normalized_macros)

# Function to recommend recipes
def recommend_recipes(target_macros, n_recommendations=10):
    """
    Recommend recipes based on target macros using KNN.

    Includes name, macros, image, and link while avoiding duplicates.
    """
    normalized_target = scaler.transform([target_macros])
    distances, indices = knn.kneighbors(normalized_target, n_neighbors=n_recommendations)

    seen_names = set()
    results = []

    for idx, dist in zip(indices[0], distances[0]):
        recipe = recipes_df.iloc[idx]
        if recipe["name"] not in seen_names:
            seen_names.add(recipe["name"])
            results.append({
                "name": recipe["name"],
                "calories": recipe["calories"],
                "protein": recipe["protein"],
                "carbs": recipe["carbs"],
                "fats": recipe["fats"],
                "distance": dist,
                "image": recipe.get("image", ""),  # Add image URL if available
                "url": recipe.get("url", "#"),     # Add recipe link if available
            })

    return results


# Route for the homepage
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Extract target macros from form input
        total_calories = float(request.form["calories"])
        total_protein = float(request.form["protein"])
        total_carbs = float(request.form["carbs"])
        total_fats = float(request.form["fats"])
        meals_per_day = int(request.form.get("meals", 3))  # Default to 3 meals

        # Calculate per-meal macros
        target_macros = {
            "calories": int(total_calories / meals_per_day),
            "protein": int(total_protein / meals_per_day),
            "carbs": int(total_carbs / meals_per_day),
            "fats": int(total_fats / meals_per_day),
        }

        # Get recommendations
        recommendations = recommend_recipes(
            [target_macros["calories"], target_macros["protein"], target_macros["carbs"], target_macros["fats"]]
        )

        # Render results
        return render_template("results.html", recipes=recommendations, target_macros=target_macros)

    return render_template("index.html")


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
