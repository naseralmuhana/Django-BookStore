from django import forms
from main import models as main_models


class BookForm(forms.ModelForm):

    image = forms.ImageField(required=True)
    for_age = forms.IntegerField(required=False)
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={"placeholder": "Add a description for this book", }
        ),
    )

    class Meta:
        model = main_models.Book
        fields = "__all__"
        exclude = ["favourite", "slug"]
        widgets = {
            'Publication_date': forms.DateInput(attrs={'placeholder': 'Select a date', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields["authors"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["authors"].help_text = ""
        self.fields["authors"].queryset = main_models.Author.objects.all()
        self.fields["categories"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["categories"].help_text = ""
        self.fields["categories"].queryset = main_models.Category.objects.all()


class CategoryForm(forms.ModelForm):

    image = forms.ImageField(required=True)

    class Meta:
        model = main_models.Category
        fields = "__all__"
        exclude = ["slug"]


class AuthorForm(forms.ModelForm):

    image = forms.ImageField(required=True)
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"placeholder": "Add a description for this auhtor", }
        ),
    )

    class Meta:
        model = main_models.Author
        fields = "__all__"
        exclude = ["slug"]


class LanguageForm(forms.ModelForm):

    image = forms.ImageField(required=True)

    class Meta:
        model = main_models.Language
        fields = "__all__"
        exclude = ["slug"]


class YearForm(forms.ModelForm):

    class Meta:
        model = main_models.Year
        fields = "__all__"
        exclude = ["slug"]
