-- upgrade --
CREATE TABLE IF NOT EXISTS "body_locations" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "ru_name" VARCHAR(255) NOT NULL,
    "eng_name" VARCHAR(255) NOT NULL,
    "parent_id" INT REFERENCES "body_locations" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "symptoms" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "ru_name" VARCHAR(255) NOT NULL,
    "eng_name" VARCHAR(255) NOT NULL,
    "has_red_flag" BOOL NOT NULL,
    "prof_name" VARCHAR(255) NOT NULL  DEFAULT '',
    "ru_synonyms" JSONB NOT NULL,
    "eng_synonyms" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(255),
    "first_name" VARCHAR(255),
    "last_name" VARCHAR(255),
    "male" BOOL,
    "age" INT,
    "country" VARCHAR(255),
    "city" VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "symptom_locations" (
    "symptoms_id" INT NOT NULL REFERENCES "symptoms" ("id") ON DELETE CASCADE,
    "bodylocations_id" INT NOT NULL REFERENCES "body_locations" ("id") ON DELETE CASCADE
);
