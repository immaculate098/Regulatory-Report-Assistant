from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            "id",
            "raw_report",
            "drug",
            "adverse_events",
            "severity",
            "outcome",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class ProcessReportSerializer(serializers.Serializer):
    report = serializers.CharField()


class TranslateSerializer(serializers.Serializer):
    outcome = serializers.CharField()
    language = serializers.ChoiceField(choices=[("fr", "French"), ("sw", "Swahili")])

