from django.db import models

# Create your models here.

class CalculationHistory(models.Model):
    expression = models.CharField(max_length=200)
    result = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.expression} = {self.result}"