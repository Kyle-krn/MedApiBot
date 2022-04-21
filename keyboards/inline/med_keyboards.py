from aiogram import types
from models.models import BodyLocations

async def choice_body_location(language):
    general_location = await BodyLocations.filter(parent_id__isnull=True)