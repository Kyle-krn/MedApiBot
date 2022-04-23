-- upgrade --
ALTER TABLE "settings_payments" ADD "eng_label" VARCHAR(255);
ALTER TABLE "settings_payments" RENAME COLUMN "label" TO "ru_label";
-- downgrade --
ALTER TABLE "settings_payments" RENAME COLUMN "ru_label" TO "label";
ALTER TABLE "settings_payments" DROP COLUMN "eng_label";
