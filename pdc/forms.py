from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class ContactForm(forms.Form):
    SUBJECTS = [
        ('general', 'General information'),
        ('contribute', 'Donating and volunteering'),
        ('join', 'Joining PDC'),
        ('voting', 'Information or Assistance with Voting'),
        ('technical', 'Technical issues with website'),
    ]

    your_name = forms.CharField(label='Your name', max_length=100)
    email = forms.EmailField(label='Email address')
    phone = forms.CharField(
        label='Phone number (optional)',
        max_length=20,
        required=False
    )
    subject = forms.CharField(
        label='Subject',
        widget=forms.Select(choices=SUBJECTS)
    )
    message = forms.CharField(
        label='Your message',
        max_length=2048,
        widget=forms.Textarea
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label="")
