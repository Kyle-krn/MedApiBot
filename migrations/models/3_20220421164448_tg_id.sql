-- upgrade --
ALTER TABLE "users" ADD "tg_id" BIGINT NOT NULL;
-- downgrade --
ALTER TABLE "users" DROP COLUMN "tg_id";
