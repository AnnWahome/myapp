from extensions import db, bcrypt
import hashlib
import secrets
import json


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    bcrypt_hash = db.Column(db.String(128), nullable=True)

    # MD5 (all 500)
    md5_salt = db.Column(db.String(32), nullable=False)
    md5_hash = db.Column(db.String(32), nullable=False)

    # SHA-256 (all 500)
    sha256_salt = db.Column(db.String(32), nullable=False)
    sha256_hash = db.Column(db.String(64), nullable=False)

    def _set_salted_hash(self, password: str, algo) -> tuple[str, str]:
        salt = secrets.token_hex(16)
        digest = algo((salt + password).encode()).hexdigest()
        return salt, digest

    def set_md5(self, password: str) -> None:
        self.md5_salt, self.md5_hash = self._set_salted_hash(password, hashlib.md5)

    def set_sha256(self, password: str) -> None:
        self.sha256_salt, self.sha256_hash = self._set_salted_hash(password, hashlib.sha256)

    def set_bcrypt(self, password: str) -> None:
        pw_hash = bcrypt.generate_password_hash(password, rounds=12)
        self.bcrypt_hash = pw_hash.decode("utf-8")

    def _check_bcrypt(self, password: str) -> bool:
        try:
            return bcrypt.check_password_hash(self.bcrypt_hash, password)
        except ValueError:
            return False

    def _check_salted(self, password: str, salt: str, stored_hash: str, algo) -> bool:
        return algo((salt + password).encode()).hexdigest() == stored_hash

    def check_password(self, password: str) -> bool:
        return any([
            self.bcrypt_hash and self._check_bcrypt(password),
            self.sha256_hash and self._check_salted(password, self.sha256_salt, self.sha256_hash, hashlib.sha256),
            self.md5_hash and self._check_salted(password, self.md5_salt, self.md5_hash, hashlib.md5),
        ])


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(300), nullable=False)
    cuisine = db.Column(db.String(120), nullable=False)
    is_vegetarian = db.Column(db.Boolean, nullable=False, default=False)
    summary = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)

    def to_summary(self):
        return {
            "id": self.id,
            "title": self.title,
            "image": self.image,
            "cuisine": self.cuisine,
            "is_vegetarian": self.is_vegetarian,
        }

    def to_dict(self):
        try:
            ingredients = json.loads(self.ingredients)
        except (ValueError, TypeError):
            ingredients = []

        return {
            "id": self.id,
            "title": self.title,
            "image": self.image,
            "cuisine": self.cuisine,
            "is_vegetarian": self.is_vegetarian,
            "summary": self.summary,
            "instructions": self.instructions,
            "extendedIngredients": ingredients,
        }
