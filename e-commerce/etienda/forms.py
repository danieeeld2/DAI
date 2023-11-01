from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def title_in_mayus_validator(value):
    if value[0].islower():
        raise ValidationError(
            _("%(value)s debe empezar con mayúscula"),
            params={"value": value},
        )

class ProductoForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100, validators=[title_in_mayus_validator])
    category = forms.CharField(label="Category", max_length=100)
    description = forms.CharField(label="Description", max_length=100)
    price = forms.DecimalField(label="Price")
    image = forms.FileField(label="Image")  
