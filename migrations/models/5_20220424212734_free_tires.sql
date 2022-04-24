-- upgrade --
ALTER TABLE "users" ADD "free_tries" INT NOT NULL  DEFAULT 0;
-- downgrade --
ALTER TABLE "users" DROP COLUMN "free_tries";
