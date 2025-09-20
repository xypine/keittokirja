from sqlite3 import Connection


class NewStep:
    created_by: int
    recipe_id: int
    summary: str
    details: str

    def __init__(
        self,
        created_by: int,
        recipe_id: int,
        summary: str,
        details: str,
    ) -> None:
        self.created_by = created_by
        self.recipe_id = recipe_id
        self.summary = summary
        self.details = details

    def insert(self, db: Connection):
        db.execute(
            """
            INSERT INTO recipe_step
            (recipe_id, summary, details, created_by) VALUES (?, ?, ?, ?)
            """,
            [
                self.recipe_id,
                self.summary,
                self.details,
                self.created_by,
            ],
        )
        db.commit()


class Step:
    id: int
    recipe_id: int
    summary: str
    details: str

    def __init__(
        self,
        id: int,
        recipe_id: int,
        summary: str,
        details: str,
    ):
        self.id = id
        self.recipe_id = recipe_id
        self.summary = summary
        self.details = details

    @staticmethod
    def delete(db: Connection, id: int, recipe_id: int, user_id: int):
        db.execute(
            """
            DELETE FROM recipe_step
            WHERE
                id = ?
                AND recipe_id = ?
                AND created_by = ?
            """,
            [id, recipe_id, user_id],
        )
        db.commit()

    def put(self, db: Connection, user_id: int):
        db.execute(
            """
            UPDATE recipe_step
            SET
                summary = ?,
                details = ?
            WHERE
                id = ?
                AND recipe_id = ?
                AND created_by = ?
            """,
            [self.summary, self.details, self.id, self.recipe_id, user_id],
        )
        db.commit()
