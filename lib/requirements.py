from sqlite3 import Connection
from typing import Optional

from lib.errors import UserError


class Requirement:
    id: int
    name: str
    amount: str
    extra_info: Optional[str]
    ingredient_link: Optional[str]
    recipe_link: Optional[str]

    def __init__(
        self,
        id: int,
        name: str,
        amount: str,
        extra_info: Optional[str],
        ingredient_id: Optional[int],
        ingredient_recipe_slug: Optional[str],
    ):
        self.id = id
        self.name = name
        self.amount = amount
        self.extra_info = extra_info
        if ingredient_id:
            self.ingredient_link = f"/ingredients#{ingredient_id}"
        if ingredient_recipe_slug:
            self.recipe_link = f"/recipes/{ingredient_recipe_slug}"

    @staticmethod
    def delete(db: Connection, id: int, recipe_id: int, user_id: int):
        db.execute(
            """
            DELETE FROM recipe_requirement
            WHERE
                id = ?
                AND recipe_id = ?
                AND created_by = ?
            """,
            [id, recipe_id, user_id],
        )
        db.commit()


class NewRequirement:
    created_by: int
    recipe_id: int
    amount: str
    extra_info: Optional[str]
    ingredient_id: Optional[int]
    ingredient_recipe_id: Optional[int]

    def __init__(
        self,
        created_by: int,
        recipe_id: int,
        amount: str,
        extra_info: Optional[str],
        ingredient_id: Optional[str],
        ingredient_recipe_id: Optional[str],
    ) -> None:
        self.created_by = created_by
        self.recipe_id = recipe_id
        self.amount = amount.strip()
        self.extra_info = extra_info.strip() if extra_info is not None else None

        match [bool(ingredient_id), bool(ingredient_recipe_id)]:
            case [True, True]:
                raise UserError(
                    "Either ingredient_id or ingredient_recipe_id must be set"
                )
            case [False, False]:
                raise UserError(
                    "ingredient_id and ingredient_recipe_id can't both be set"
                )

        if ingredient_id:
            self.ingredient_id = int(ingredient_id)
        else:
            self.ingredient_id = None

        if ingredient_recipe_id:
            self.ingredient_recipe_id = int(ingredient_recipe_id)
        else:
            self.ingredient_recipe_id = None

    def insert(self, db: Connection):
        db.execute(
            """
            INSERT INTO recipe_requirement
            (recipe_id, ingredient_id, amount, extra_info, ingredient_recipe_id, created_by) VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                self.recipe_id,
                self.ingredient_id,
                self.amount,
                self.extra_info,
                self.ingredient_recipe_id,
                self.created_by,
            ],
        )
        db.commit()
