CREATE TABLE recipe (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	name TEXT NOT NULL UNIQUE,
	slug TEXT NOT NULL UNIQUE,
	created_by INTEGER NOT NULL,
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (created_by) REFERENCES user (id)
);

CREATE TABLE recipe_requirement (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,

	recipe_id INTEGER NOT NULL,
	-- Requirements can either reference raw ingredients
	ingredient_id INTEGER,
	-- or other recipes
	ingredient_recipe_id INTEGER,
	amount TEXT NOT NULL,
	extra_info TEXT,

	created_by INTEGER NOT NULL,
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

	FOREIGN KEY (recipe_id) REFERENCES recipe (id),
	FOREIGN KEY (ingredient_id) REFERENCES ingredient (id),
	FOREIGN KEY (ingredient_recipe_id) REFERENCES recipe (id),
	CONSTRAINT recipe_ingredient_reference CHECK (
    (ingredient_id IS NOT NULL AND ingredient_recipe_id IS NULL) OR
    (ingredient_id IS NULL AND ingredient_recipe_id IS NOT NULL)
	),

	FOREIGN KEY (created_by) REFERENCES users (id)
);

CREATE UNIQUE INDEX idx_recipe_ingredient
ON recipe_requirement(recipe_id, ingredient_id)
WHERE ingredient_id IS NOT NULL;

CREATE UNIQUE INDEX idx_recipe_ingredient_recipe
ON recipe_requirement(recipe_id, ingredient_recipe_id)
WHERE ingredient_recipe_id IS NOT NULL;

CREATE TABLE recipe_step (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	recipe_id INTEGER NOT NULL,
	summary TEXT NOT NULL,
	details TEXT,

	created_by INTEGER NOT NULL,
	created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

	FOREIGN KEY (recipe_id) REFERENCES recipe (id),
	FOREIGN KEY (created_by) REFERENCES users (id)
)
