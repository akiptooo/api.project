from django.db import models


class Case(models.Model):
    CASE_TYPES = [
        ("Civil", "Civil"),
        ("Criminal", "Criminal"),
        ("Family", "Family"),
        ("Commercial", "Commercial"),
    ]

    case_number = models.CharField(max_length=50, unique=True)
    case_type = models.CharField(max_length=20, choices=CASE_TYPES)
    plaintiff = models.CharField(max_length=100)
    defendant = models.CharField(max_length=100)
    judge = models.CharField(max_length=100)
    hearing_date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.case_number
