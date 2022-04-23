-- upgrade --
CREATE TABLE IF NOT EXISTS "settings_payments" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "label" VARCHAR(255) NOT NULL,
    "amount" INT NOT NULL,
    "url_photo" TEXT NOT NULL
);
-- downgrade --
DROP TABLE IF EXISTS "settings_payments";
