from django import forms


class SearchForm(forms.Form):
    number = forms.CharField(max_length=255)


class EditForm(forms.Form):
    summary = forms.Field()

    def __init__(self, document, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        if 'summary' in document.keys():
            self.summary = document['summary']
            self.fields['summary'] = forms.CharField(initial=document['summary'],
                                                     widget=forms.widgets.Textarea())
