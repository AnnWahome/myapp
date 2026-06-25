from flask import Blueprint, jsonify, request
from sqlalchemy import func
from models import Recipe

recipes_bp = Blueprint("recipes", __name__)


@recipes_bp.route("/api/recipes/popular", methods=["GET"])
def popular_recipes():
    recipes = Recipe.query.order_by(func.random()).limit(9).all()
    return jsonify([recipe.to_summary() for recipe in recipes])


@recipes_bp.route("/api/recipes/vegetarian", methods=["GET"])
def vegetarian_recipes():
    recipes = Recipe.query.filter_by(is_vegetarian=True).limit(9).all()
    return jsonify([recipe.to_summary() for recipe in recipes])


@recipes_bp.route("/api/recipes/cuisine/<string:cuisine>", methods=["GET"])
def cuisine_recipes(cuisine):
    recipes = Recipe.query.filter(Recipe.cuisine.ilike(cuisine)).all()
    return jsonify([recipe.to_summary() for recipe in recipes])


@recipes_bp.route("/api/recipes/search", methods=["GET"])
def search_recipes():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify([])

    recipes = Recipe.query.filter(Recipe.title.ilike(f"%{query}%"))
    return jsonify([recipe.to_summary() for recipe in recipes])


@recipes_bp.route("/api/recipes/<int:recipe_id>", methods=["GET"])
def recipe_detail(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"message": "Recipe not found"}), 404
    return jsonify(recipe.to_dict())
