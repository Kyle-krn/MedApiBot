from tortoise import Model, fields


class UserModel(Model):
    id: int = fields.IntField(pk=True)
    tg_id: int = fields.BigIntField()
    username: str = fields.CharField(max_length=255, null=True)
    first_name: str = fields.CharField(max_length=255, null=True)
    last_name: str = fields.CharField(max_length=255, null=True)
    male: bool = fields.BooleanField(null=True)
    year_of_birth: int = fields.IntField(null=True)
    language: str = fields.CharField(max_length=10, null=True)
    location: str = fields.CharField(max_length=255, null=True)

    symptoms: fields.ManyToManyRelation["Symptoms"]
    
    class Meta:
        table = "users"





class BodyLocations(Model):
    id: int = fields.IntField(pk=True)
    ru_name = fields.CharField(max_length=255)
    eng_name = fields.CharField(max_length=255)
    parent: fields.ForeignKeyNullableRelation["BodyLocations"] = fields.ForeignKeyField(
        "models.BodyLocations", related_name="location", null=True, on_delete="SET NULL"
    )
    location: fields.ReverseRelation["BodyLocations"]
    symptoms: fields.ManyToManyRelation["Symptoms"]
    
    class Meta:
        table = 'body_locations'

    def __str__(self):
        return self.ru_name


class Symptoms(Model):
    id: int = fields.IntField(pk=True)
    ru_name = fields.CharField(max_length=255)
    eng_name = fields.CharField(max_length=255)
    has_red_flag = fields.BooleanField()
    prof_name = fields.CharField(max_length=255, default="")
    ru_synonyms = fields.JSONField()
    eng_synonyms = fields.JSONField()

    locations: fields.ManyToManyRelation[BodyLocations] = fields.ManyToManyField(
        "models.BodyLocations", related_name="symptoms", through="symptom_locations"
    )

    user: fields.ManyToManyRelation[UserModel] = fields.ManyToManyField(
        "models.UserModel", related_name="symptoms", through="symptom_user", backward_key="symptom_id", forward_key="user_id"
    )

    class Meta:
        table = 'symptoms'

    def __str__(self):
        return self.ru_name


class UserSymptoms(Model):
    id: int = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.UserModel")
    symptom = fields.ForeignKeyField("models.Symptoms")
    sublocation = fields.ForeignKeyField("models.BodyLocations")

    class Meta:
        table = 'symptom_user'


class TextModel(Model):
    id: int = fields.IntField(pk=True)
    short_description: str = fields.CharField(max_length=255, null=True)
    ru_text: str = fields.TextField()
    eng_text: str = fields.TextField(null=True)

    class Meta:
        table = 'text'

    def __str__(self):
        return self.short_description


class TextButtonModel(Model):
    id: int = fields.IntField(pk=True)
    short_description: str = fields.CharField(max_length=255, null=True)
    ru_text: str = fields.TextField()
    eng_text: str = fields.TextField(null=True)

    class Meta:
        table = 'button_text'

    def __str__(self):
        return self.short_description


class SuccessPayments(Model):
    id: int = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.UserModel")
    symptom_array = fields.JSONField()
    diagnosis = fields.TextField(null=True)
    amount = fields.IntField()


class SettingsPayments(Model):
    id: int = fields.IntField(pk=True)
    ru_label: str = fields.CharField(max_length=255)
    eng_label: str = fields.CharField(max_length=255, null=True)
    amount: int = fields.IntField()
    url_photo = fields.TextField()


    class Meta:
        table = 'settings_payments'