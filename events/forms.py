from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class RsvpForm(forms.Form):
    """
    Displays a form for RSVPing to an event occurrence
    """
    event_occurrence_id = forms.IntegerField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField(
        label='Phone number (optional)',
        max_length=20,
        required=False
    )
    number_attending = forms.IntegerField(initial=1)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label="")
