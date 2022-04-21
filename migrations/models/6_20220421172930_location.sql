-- upgrade --
ALTER TABLE "users" ADD "language" VARCHAR(10);
ALTER TABLE "users" DROP COLUMN "country";
-- downgrade --
ALTER TABLE "users" ADD "country" VARCHAR(255);
ALTER TABLE "users" DROP COLUMN "language";
