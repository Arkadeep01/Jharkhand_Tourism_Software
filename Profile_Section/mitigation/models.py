from datetime import datetime
from tortoise import fields, models

class Mitigation(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    risk_level = fields.CharField(max_length=50)  # e.g., Low, Medium, High
    created_at = fields.DatetimeField(default=datetime.utcnow)
    updated_at = fields.DatetimeField(default=datetime.utcnow)
    user_id = fields.IntField()  # the user/admin who created the mitigation

    def __str__(self):
        return self.title
