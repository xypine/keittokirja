from dataclasses import dataclass
from datetime import datetime
from sqlite3 import Connection

from lib.errors import UserError


@dataclass
class Ingredient:
    id: int
    name: str
    created_by: int
    created_at: datetime
    updated_at: datetime
    creator_name: str | None
    in_use: int

    @staticmethod
    def get(
        db: Connection, created_by: str | None = None, name_like: str | None = None
    ):
        name_like = f"%{name_like}%" if name_like is not None else None
        rows = db.execute(
            """
                SELECT
                    i.id, i.name, i.created_by, i.created_at, i.updated_at, u.username,
                    (SELECT COUNT(*) FROM recipe_requirement r WHERE r.ingredient_id = i.id)
                FROM ingredient i
                LEFT JOIN user u ON u.id = i.created_by
                WHERE
                    (?1 IS NULL OR i.created_by = ?1) AND
                    (?2 IS NULL OR i.name LIKE ?2)
            """,
            [created_by, name_like],
        ).fetchall()
        return [Ingredient(*row) for row in rows]

    @staticmethod
    def delete(db: Connection, id: int, user_id: int):
        db.execute(
            """
            DELETE FROM ingredient
            WHERE
                id = ?
                AND created_by = ?
            """,
            [id, user_id],
        )
        db.commit()


class NewIngredient:
    name: str
    created_by: int

    def __init__(self, name: str, created_by: int):
        self.name = name.strip()
        if len(self.name) < 3:
            raise UserError("name must be at least 3 characters long")

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
        return Ingredient(
            id,
            name,
            created_by,
            created_at,
            updated_at,
            creator_name=None,
            in_use=False,
        )
