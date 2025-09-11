from datetime import datetime
from sqlite3 import Connection


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
    def get(
        db: Connection, created_by: str | None = None, name_like: str | None = None
    ):
        name_like = f"%{name_like}%" if name_like is not None else None
        rows = db.execute(
            """
                SELECT
                    id, name, created_by, created_at, updated_at
                FROM ingredient
                WHERE
                    (?1 IS NULL OR created_by = ?1) AND
                    (?2 IS NULL OR name LIKE ?2)
            """,
            [created_by, name_like],
        ).fetchall()
        db.close()
        return [Ingredient(*row) for row in rows]


class NewIngredient:
    name: str
    created_by: int

    def __init__(self, name: str, created_by: int):
        self.name = name
        self.created_by = created_by

    def insert(self, db: Connection) -> Ingredient:
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
