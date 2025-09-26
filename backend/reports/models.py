from django.db import models


class Report(models.Model):
    raw_report = models.TextField()
    drug = models.CharField(max_length=255, blank=True)
    adverse_events = models.JSONField(default=list, blank=True)
    severity = models.CharField(max_length=32, blank=True)
    outcome = models.CharField(max_length=32, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Report {self.id} - {self.drug or 'Unknown Drug'}"

# Create your models here.
