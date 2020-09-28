from django import forms
from .models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control rounded-0', 'rows': "3", 'placeholder': "message", "autocomplete": "off"})
        }

        def clean_message(self):
            message = self.cleaned_data.get('message')
            if len(message) > 200:
                raise forms.ValidationError('Too way heavy')
            return message
