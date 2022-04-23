-- upgrade --
CREATE TABLE IF NOT EXISTS "successpayments" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "symptom_array" JSONB NOT NULL,
    "diagnosis" TEXT,
    "amount" INT NOT NULL,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
-- downgrade --
DROP TABLE IF EXISTS "successpayments";
