from datetime import datetime
from sqlite3 import Connection
from typing import List
from src.steps import Step
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
    steps: List[Step]

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
        steps: List[Step],
    ):
        self.id = id
        self.name = name
        self.slug = slug
        self.created_by = created_by
        self.created_at = created_at
        updated_at = updated_at
        self.creator_name = creator_name
        self.ingredients = ingredients
        self.steps = steps

    @staticmethod
    def get_by_slug(db: Connection, slug: str):
        rows = db.execute(
            """
                WITH correct_recipe AS (
                    SELECT * FROM recipe WHERE slug = ?1
                ),
                correct_requirements AS (
                    SELECT
                        rr.*,
                        COALESCE(ingredient.name, ir.name) AS "rname",
                        ir.slug AS "slug"
                    FROM recipe_requirement rr
                    JOIN correct_recipe ON rr.recipe_id = correct_recipe.id
                    LEFT JOIN ingredient ON ingredient.id = rr.ingredient_id
                    LEFT JOIN recipe ir ON ir.id = rr.ingredient_recipe_id
                ),
                correct_steps AS (
                  SELECT *
                  FROM recipe_step rs
                  JOIN correct_recipe ON rs.recipe_id = correct_recipe.id
                )
                SELECT
                    r.id, r.name, r.slug, r.created_by, r.created_at, r.updated_at, u.username,
                    rr.id, rr.rname, rr.amount, rr.extra_info, rr.ingredient_id, rr.slug,
                    rs.id, rs.summary, rs.details
                FROM correct_recipe r
                LEFT JOIN correct_requirements rr
                LEFT JOIN correct_steps rs
                LEFT JOIN user u ON u.id = r.created_by
            """,
            [slug],
        ).fetchall()
        [id, name, slug, created_by, created_at, updated_at, creator_name] = rows[0][:7]

        def ingredientGenerator():
            seen_ids = []
            for r in rows:
                id = r[7]
                if r[7] and not (id in seen_ids):
                    yield Requirement(r[7], r[8], r[9], r[10], r[11], r[12])
                    seen_ids.append(id)

        ingredients = list(ingredientGenerator())

        def stepGenerator():
            seen_ids = []
            for r in rows:
                id = r[13]
                if r[0] and id and not (id in seen_ids):
                    yield Step(id, r[0], r[14], r[15])
                    seen_ids.append(id)

        steps = list(stepGenerator())

        return Recipe(
            id,
            name,
            slug,
            created_by,
            created_at,
            updated_at,
            creator_name,
            ingredients,
            steps,
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
