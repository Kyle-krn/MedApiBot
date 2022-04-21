-- upgrade --
ALTER TABLE "users" RENAME COLUMN "age" TO "year_of_birth";
-- downgrade --
ALTER TABLE "users" RENAME COLUMN "year_of_birth" TO "age";
