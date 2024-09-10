from django.db import models

class Enterprise(models.Model):
    corporate_reason = models.CharField(max_length=80)
    trade_name = models.CharField(max_length=80)
    identification_number = models.CharField(max_length=14)

    def __str__(self) -> str:
        return str(self.trade_name)
