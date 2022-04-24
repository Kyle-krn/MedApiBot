-- upgrade --
ALTER TABLE "users" RENAME COLUMN "location" TO "location_country";
-- downgrade --
ALTER TABLE "users" RENAME COLUMN "location_country" TO "location";
