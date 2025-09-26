from typing import List

import re
import spacy
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Report
from .serializers import (
    ReportSerializer,
    ProcessReportSerializer,
    TranslateSerializer,
)


_NLP = spacy.load("en_core_web_sm")

SEVERITY_KEYWORDS = {
    "severe": ["severe", "life-threatening", "intense"],
    "moderate": ["moderate", "medium"],
    "mild": ["mild", "slight"],
}

OUTCOME_KEYWORDS = {
    "recovered": ["recovered", "resolved", "better"],
    "ongoing": ["ongoing", "continuing", "persisting", "stable"],
    "fatal": ["fatal", "death", "died"],
}

ADVERSE_EVENT_SYNONYMS = {
    "nausea": ["nausea", "queasy", "vomit", "vomiting"],
    "headache": ["headache", "migraine"],
    "dizziness": ["dizziness", "vertigo", "lightheaded"],
    "rash": ["rash", "hives", "urticaria"],
    "fever": ["fever", "pyrexia", "temperature"],
    "cough": ["cough", "coughing"],
    "fatigue": ["fatigue", "tired", "exhausted"],
}


def _extract_drug(text: str) -> str:
    doc = _NLP(text)
    candidates: List[str] = []
    for ent in doc.ents:
        if ent.label_ in {"PRODUCT", "DRUG", "ORG"}:
            candidates.append(ent.text)
    # Simple regex for "Drug X" patterns
    m = re.search(r"\bDrug\s+([A-Z][\w-]*)", text)
    if m:
        candidates.append(f"Drug {m.group(1)}")
    return candidates[0] if candidates else ""


def _extract_adverse_events(text: str) -> List[str]:
    text_lower = text.lower()
    found: List[str] = []
    for canonical, variants in ADVERSE_EVENT_SYNONYMS.items():
        for v in variants:
            if re.search(rf"\b{re.escape(v)}\b", text_lower):
                found.append(canonical)
                break
    # fallback by looking for common symptom POS patterns (optional, simple)
    return sorted(list(dict.fromkeys(found)))


def _extract_severity(text: str) -> str:
    text_lower = text.lower()
    for sev, keys in SEVERITY_KEYWORDS.items():
        for k in keys:
            if k in text_lower:
                return sev
    return ""


def _extract_outcome(text: str) -> str:
    text_lower = text.lower()
    for outcome, keys in OUTCOME_KEYWORDS.items():
        for k in keys:
            if k in text_lower:
                return outcome
    return ""


@api_view(["POST"])
def process_report(request):
    serializer = ProcessReportSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    raw = serializer.validated_data["report"]

    drug = _extract_drug(raw)
    adverse_events = _extract_adverse_events(raw)
    severity = _extract_severity(raw)
    outcome = _extract_outcome(raw)

    report = Report.objects.create(
        raw_report=raw,
        drug=drug,
        adverse_events=adverse_events,
        severity=severity,
        outcome=outcome,
    )

    return Response(
        ReportSerializer(report).data,
        status=status.HTTP_200_OK,
    )


class ReportsListView(generics.ListAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


@api_view(["POST"])
def translate_outcome(request):
    serializer = TranslateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    outcome = serializer.validated_data["outcome"].lower()
    lang = serializer.validated_data["language"]

    translations = {
        "fr": {
            "recovered": "rétabli",
            "ongoing": "en cours",
            "fatal": "fatal",
        },
        "sw": {
            "recovered": "amepona",
            "ongoing": "inaendelea",
            "fatal": "mbaya",
        },
    }
    translated = translations.get(lang, {}).get(outcome, outcome)
    return Response({"outcome": outcome, "language": lang, "translated": translated})

# Create your views here.
