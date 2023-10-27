from django import forms

class ProductoForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    category = forms.CharField(label="Category", max_length=100)
    description = forms.CharField(label="Description", max_length=100)
    price = forms.DecimalField(label="Price")
    image = forms.FileField(label="Image")  

