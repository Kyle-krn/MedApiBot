-- upgrade --
ALTER TABLE "users" RENAME COLUMN "city" TO "location";
ALTER TABLE "users" DROP COLUMN "language";
-- downgrade --
ALTER TABLE "users" RENAME COLUMN "location" TO "city";
ALTER TABLE "users" ADD "language" VARCHAR(10);
