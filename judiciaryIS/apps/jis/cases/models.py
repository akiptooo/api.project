from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Case(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Review'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
        CLOSED = 'CLOSED', 'Closed'
        DISMISSED = 'DISMISSED', 'Dismissed'

    class CaseType(models.TextChoices):
        CIVIL = 'CIVIL', 'Civil'
        CRIMINAL = 'CRIMINAL', 'Criminal'
        FAMILY = 'FAMILY', 'Family'
        COMMERCIAL = 'COMMERCIAL', 'Commercial'
        PROBATE = 'PROBATE', 'Probate'
        ADMINISTRATIVE = 'ADMINISTRATIVE', 'Administrative'

    title = models.CharField(max_length=200)
    description = models.TextField()
    case_number = models.CharField(max_length=50, unique=True, blank=True)
    filed_by_lawyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='filed_cases')
    date_filed = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    case_type = models.CharField(max_length=20, choices=CaseType.choices, default=CaseType.CIVIL)
    assigned_judge = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                     related_name='assigned_cases', limit_choices_to={'role': 'JUDGE'})
    priority = models.CharField(max_length=10, choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], default='MEDIUM')
    
    def save(self, *args, **kwargs):
        if not self.case_number:
            # Generate case number: YYYY-MM-XXXX
            year = self.date_filed.strftime('%Y')
            last_case = Case.objects.filter(date_filed__year=year).order_by('-id').first()
            last_number = int(last_case.case_number.split('-')[-1]) if last_case else 0
            self.case_number = f"{year}-{str(last_number + 1).zfill(4)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.case_number}: {self.title}"

class Document(models.Model):
    class DocumentType(models.TextChoices):
        PLEADING = 'PLEADING', 'Pleading'
        EVIDENCE = 'EVIDENCE', 'Evidence'
        ORDER = 'ORDER', 'Order'
        JUDGMENT = 'JUDGMENT', 'Judgment'
        MOTION = 'MOTION', 'Motion'
        AFFIDAVIT = 'AFFIDAVIT', 'Affidavit'

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=DocumentType.choices)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    file_path = models.CharField(max_length=500)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.case.case_number}"

class Hearing(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='hearings')
    hearing_date = models.DateTimeField()
    hearing_type = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=200)
    presiding_judge = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'JUDGE'})
    notes = models.TextField(blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Hearing for {self.case.case_number} on {self.hearing_date.strftime('%Y-%m-%d')}"
