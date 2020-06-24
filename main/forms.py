from django import forms
from main import models as main_models


class AddBookForm(forms.ModelForm):

    class Meta:
        model = main_models.Book
        fields = "__all__"
        exclude = ["favourite", "slug"]


    def __init__(self, *args, **kwargs):
        super(AddBookForm, self).__init__(*args, **kwargs)
        self.fields["authors"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["authors"].help_text = ""
        self.fields["authors"].queryset = main_models.Author.objects.all()
        self.fields["categories"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["categories"].help_text = ""
        self.fields["categories"].queryset = main_models.Category.objects.all()


class AddCategoryForm(forms.ModelForm):

    class Meta:
        model = main_models.Category
        fields = "__all__"


class AddAuthorForm(forms.ModelForm):

    class Meta:
        model = main_models.Author
        fields = "__all__"


class AddLanguageForm(forms.ModelForm):

    class Meta:
        model = main_models.Language
        fields = "__all__"


class AddYearForm(forms.ModelForm):

    class Meta:
        model = main_models.Year
        fields = "__all__"
