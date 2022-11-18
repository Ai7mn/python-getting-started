from django import forms


class AddForm(forms.Form):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        fields = ('images' ,)

    def save(self, commit=True):
        images = self.cleaned_data.pop('images')
        return images