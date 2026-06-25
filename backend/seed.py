import csv
import json
import random
import secrets
from faker import Faker

from app import create_app
from extensions import db
from models import Recipe, User


def seed_users(count=500, csv_out=None):
    fake = Faker()
    created = 0
    usernames = set(u.username for u in User.query.with_entities(User.username).all())
    rows = []

    while created < count:
        first = fake.first_name().lower()
        last = fake.last_name().lower()
        username = f"{first}.{last}"
        if username in usernames:
            username = f"{username}{secrets.randbelow(9999)}"
        if username in usernames:
            continue

        password = secrets.token_urlsafe(8)
        user = User(username=username)
        user.set_md5(password)
        user.set_sha256(password)

        if created < 50:
            user.set_bcrypt(password)

        db.session.add(user)
        usernames.add(username)
        rows.append({"username": username, "password": password})
        created += 1

    db.session.commit()

    if csv_out:
        with open(csv_out, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=["username", "password"])
            writer.writeheader()
            writer.writerows(rows)

    print(f"Created {created} users successfully")


def slugify(value: str) -> str:
    return "".join(c for c in value.lower().replace(" ", "-") if c.isalnum() or c == "-")


def seed_recipes(count=45):
    if Recipe.query.count() > 0:
        print("Recipes already seeded. Skipping recipe seed.")
        return

    fake = Faker()
    cuisine_types = [
        "Italian",
        "Mexican",
        "Indian",
        "Japanese",
        "Thai",
        "French",
        "Mediterranean",
        "American",
        "Chinese",
        "Vegetarian",
    ]

    protein_items = [
        "chicken breast",
        "tofu",
        "cremini mushrooms",
        "black beans",
        "chickpeas",
        "salmon fillet",
        "shrimp",
        "eggplant",
        "zucchini",
        "lentils",
    ]

    vegetable_items = [
        "spinach",
        "bell peppers",
        "broccoli florets",
        "kale",
        "carrots",
        "tomatoes",
        "red onions",
        "asparagus",
        "snap peas",
        "sweet potatoes",
    ]

    pantry_items = [
        "olive oil",
        "soy sauce",
        "garlic cloves",
        "ginger",
        "basil",
        "cilantro",
        "cumin",
        "chili flakes",
        "lemon juice",
        "coconut milk",
    ]

    measuring_items = [
        "1 cup",
        "2 tablespoons",
        "3 cloves",
        "1 teaspoon",
        "2 cups",
        "1/2 cup",
        "4 tablespoons",
        "1 slice",
        "3 sprigs",
        "1 pinch",
    ]

    main_dishes = [
        "Pasta", "Tacos", "Curry", "Stir-Fry", "Salad", "Bowl", "Stew", "Skillet", "Risotto", "Wrap"
    ]

    for index in range(1, count + 1):
        cuisine = random.choice(cuisine_types)
        is_vegetarian = cuisine == "Vegetarian" or random.random() < 0.35
        base = random.choice(main_dishes)
        adjective = fake.word().capitalize()
        title = f"{adjective} {cuisine} {base}"
        summary = fake.sentence(nb_words=18)
        instructions = "\n\n".join(fake.paragraphs(nb=random.randint(3, 5)))

        ingredients = []
        for ingredient_index in range(random.randint(6, 10)):
            if is_vegetarian:
                item = random.choice(vegetable_items + pantry_items)
            else:
                item = random.choice(protein_items + vegetable_items + pantry_items)
            quantity = random.choice(measuring_items)
            ingredients.append({
                "id": ingredient_index + 1,
                "original": f"{quantity} {item}",
            })

        image = "/food.jpg"

        recipe = Recipe(
            title=title,
            image=image,
            cuisine=cuisine,
            is_vegetarian=is_vegetarian,
            summary=summary,
            instructions=instructions,
            ingredients=json.dumps(ingredients),
        )
        db.session.add(recipe)

    db.session.commit()
    print(f"Created {count} recipes successfully")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        seed_users(500, csv_out="users.csv")
        seed_recipes(45)
