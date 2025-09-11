from datetime import datetime
from sqlite3 import Connection
from src.utils import slugify


class Recipe:
    id: int
    name: str
    slug: str
    created_by: int
    created_at: datetime
    updated_at: datetime

    creator_name: str | None

    def __init__(
        self,
        id: int,
        name: str,
        slug: str,
        created_by: int,
        created_at: datetime,
        updated_at: datetime,
        creator_name: str | None,
    ):
        self.id = id
        self.name = name
        self.slug = slug
        self.created_by = created_by
        self.created_at = created_at
        updated_at = updated_at
        self.creator_name = creator_name

    @staticmethod
    def get(
        db: Connection, created_by: str | None = None, name_like: str | None = None
    ):
        name_like = f"%{name_like}%" if name_like is not None else None
        rows = db.execute(
            """
                SELECT
                    r.id, r.name, r.slug, r.created_by, r.created_at, r.updated_at, u.username
                FROM recipe r
                LEFT JOIN user u ON u.id = r.created_by
                WHERE
                    (?1 IS NULL OR r.created_by = ?1) AND
                    (?2 IS NULL OR r.name LIKE ?2)
            """,
            [created_by, name_like],
        ).fetchall()
        db.close()
        return [Recipe(*row) for row in rows]


class NewRecipe:
    name: str
    slug: str
    created_by: int

    def __init__(self, name: str, created_by: int):
        self.name = name
        self.slug = slugify(name)
        self.created_by = created_by

    def insert(self, db: Connection) -> Recipe:
        [id, name, slug, created_by, created_at, updated_at] = db.execute(
            """
            INSERT INTO recipe
            (name, slug, created_by) VALUES (?, ?, ?)
            RETURNING id, name, slug, created_by, created_at, updated_at
        """,
            [self.name, self.slug, self.created_by],
        ).fetchone()
        db.commit()
        return Recipe(id, name, slug, created_by, created_at, updated_at)
