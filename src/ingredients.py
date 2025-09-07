from src.db import connect
from datetime import datetime


class Ingredient:
    id: int
    name: str
    created_by: int
    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        id: int,
        name: str,
        created_by: int,
        created_at: datetime,
        updated_at: datetime,
    ):
        self.id = id
        self.name = name
        self.created_by = created_by
        self.created_at = created_at
        updated_at = updated_at

    @staticmethod
    def get_all():
        db = connect()
        rows = db.execute(
            "SELECT id, name, created_by, created_at, updated_at FROM ingredient"
        ).fetchall()
        db.close()
        return [Ingredient(*row) for row in rows]


class NewIngredient:
    name: str
    created_by: int

    def __init__(self, name: str, created_by: int):
        self.name = name
        self.created_by = created_by

    def insert(self) -> Ingredient:
        db = connect()
        [id, name, created_by, created_at, updated_at] = db.execute(
            """
            INSERT INTO ingredient
            (name, created_by) VALUES (?, ?)
            RETURNING id, name, created_by, created_at, updated_at
        """,
            [self.name, self.created_by],
        ).fetchone()
        db.commit()
        return Ingredient(id, name, created_by, created_at, updated_at)


def insert_ingredient():
    pass
