from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
# ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
USER = env.str("USER_DB")  # Тоже str, но для айпи адреса хоста
PASSWORD = env.str("PASSWORD")  # Тоже str, но для айпи адреса хоста
DATABASE = env.str("DB")  # Тоже str, но для айпи адреса хоста
PORT = env.int("PORT")  # Тоже str, но для айпи адреса хоста
HOST= env.str("HOST")

PAYMENTS_TOKEN = env.str("PAYMENTS_TOKEN")

API_URL = env.str("API_URL")
API_TOKEN = env.str("API_TOKEN")

POSTGRES_URI = f"postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

TORTOISE_ORM = {
    "connections": {"default": POSTGRES_URI},
    "apps": {
        "models": {
            "models": ["models.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "UTC"
}
