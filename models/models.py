from tortoise import Model, fields


class UserModel(Model):
    id: int = fields.IntField(pk=True)
    username: str = fields.CharField(max_length=255, null=True)
    first_name: str = fields.CharField(max_length=255, null=True)
    last_name: str = fields.CharField(max_length=255, null=True)
    male: bool = fields.BooleanField(null=True)
    age: int = fields.IntField(null=True)
    country: str = fields.CharField(max_length=255, null=True)
    city: str = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "users"


class BodyLocations(Model):
    id: int = fields.IntField(pk=True)
    ru_name = fields.CharField(max_length=255)
    eng_name = fields.CharField(max_length=255)
    sublocations: fields.ReverseRelation["BodySubLocations"]
    
    class Meta:
        table = 'body_locations'

    def __str__(self):
        return self.ru_name

class BodySubLocations(Model):
    id: int = fields.IntField(pk=True)
    user: fields.ForeignKeyRelation = fields.ForeignKeyField("models.BodyLocations", related_name="sublocations")
    ru_name = fields.CharField(max_length=255)
    eng_name = fields.CharField(max_length=255)

    class Meta:
        table = 'body_sublocations'
    
    def __str__(self):
        return self.ru_name