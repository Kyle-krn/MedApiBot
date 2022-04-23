-- upgrade --
CREATE TABLE IF NOT EXISTS "button_text" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "short_description" VARCHAR(255),
    "ru_text" TEXT NOT NULL,
    "eng_text" TEXT
);
-- downgrade --
DROP TABLE IF EXISTS "button_text";
