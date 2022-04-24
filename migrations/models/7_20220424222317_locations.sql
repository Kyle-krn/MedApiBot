-- upgrade --
ALTER TABLE "users" ADD "location_city" VARCHAR(255);
-- downgrade --
ALTER TABLE "users" DROP COLUMN "location_city";
