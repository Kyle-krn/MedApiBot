-- upgrade --
CREATE TABLE IF NOT EXISTS "text" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "short_description" VARCHAR(255) NOT NULL,
    "ru_text" TEXT NOT NULL,
    "eng_text" TEXT
);
-- downgrade --
DROP TABLE IF EXISTS "text";
