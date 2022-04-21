-- upgrade --
ALTER TABLE "users" ADD "language" VARCHAR(10);
-- downgrade --
ALTER TABLE "users" DROP COLUMN "language";
