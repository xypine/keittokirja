from datetime import datetime
from sqlite3 import Connection
from typing import List
from src.utils import slugify
from src.requirements import Requirement


class RecipeListing:
    id: int
    name: str
    slug: str
    creator_name: str

    def __init__(
        self,
        id: int,
        name: str,
        slug: str,
        creator_name: str,
    ):
        self.id = id
        self.name = name
        self.slug = slug
        self.creator_name = creator_name

    @staticmethod
    def get(
        db: Connection, created_by: str | None = None, name_like: str | None = None
    ):
        name_like = f"%{name_like}%" if name_like is not None else None
        rows = db.execute(
            """
                SELECT
                    r.id, r.name, r.slug, u.username
                FROM recipe r
                LEFT JOIN user u ON u.id = r.created_by
                WHERE
                    (?1 IS NULL OR r.created_by = ?1) AND
                    (?2 IS NULL OR r.name LIKE ?2)
            """,
            [created_by, name_like],
        ).fetchall()
        db.close()
        return [RecipeListing(*row) for row in rows]


class Recipe:
    id: int
    name: str
    slug: str
    created_by: int
    created_at: datetime
    updated_at: datetime
    creator_name: str
    ingredients: List[Requirement]

    def __init__(
        self,
        id: int,
        name: str,
        slug: str,
        created_by: int,
        created_at: datetime,
        updated_at: datetime,
        creator_name: str,
        ingredients: List[Requirement],
    ):
        self.id = id
        self.name = name
        self.slug = slug
        self.created_by = created_by
        self.created_at = created_at
        updated_at = updated_at
        self.creator_name = creator_name
        self.ingredients = ingredients

    @staticmethod
    def get_by_slug(db: Connection, slug: str):
        rows = db.execute(
            """
                SELECT
                    r.id, r.name, r.slug, r.created_by, r.created_at, r.updated_at, u.username,
                    rr.id,
                    COALESCE(
                        (SELECT name FROM ingredient WHERE ingredient.id = rr.ingredient_id),
                        (SELECT name FROM recipe WHERE recipe.id = rr.ingredient_recipe_id)
                    ),
                    rr.amount, rr.ingredient_id, (SELECT slug FROM recipe WHERE recipe.id = rr.ingredient_recipe_id)
                FROM recipe r
                LEFT JOIN recipe_requirement rr ON rr.recipe_id = r.id
                LEFT JOIN user u ON u.id = r.created_by
                WHERE
                    r.slug = ?1
            """,
            [slug],
        ).fetchall()
        [id, name, slug, created_by, created_at, updated_at, creator_name] = rows[0][:7]

        def whereRequirement():
            for r in rows:
                if r[7]:
                    yield Requirement(r[7], r[8], r[9], r[10], r[11])

        ingredients = list(whereRequirement())

        return Recipe(
            id,
            name,
            slug,
            created_by,
            created_at,
            updated_at,
            creator_name,
            ingredients,
        )


class NewRecipe:
    name: str
    slug: str
    created_by: int

    def __init__(self, name: str, created_by: int):
        self.name = name
        self.slug = slugify(name)
        self.created_by = created_by

    def insert(self, db: Connection) -> str:
        db.execute(
            """
            INSERT INTO recipe
            (name, slug, created_by) VALUES (?, ?, ?)
            """,
            [self.name, self.slug, self.created_by],
        ).fetchone()
        db.commit()
        return self.slug
