from django import forms
from candidate.models import CandidateProfile
from django.forms import ModelForm
class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model=CandidateProfile
        fields=["candidate_name","DOB","qualification","skills","profile_pic","experience","cv"]
        widgets = {
            "DOB": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "candidate_name": forms.TextInput(attrs={"class": "form-control"}),
            "qualification": forms.TextInput(attrs={"class": "form-control"}),
            "skills": forms.TextInput(attrs={"class": "form-control"}),
            "experience": forms.NumberInput(attrs={"class": "form-control"}),
            }