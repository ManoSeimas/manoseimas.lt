from django import forms


class SearchForm(forms.Form):
    number = forms.CharField(max_length=255)


class EditForm(forms.Form):
    summary = forms.CharField(widget=forms.widgets.Textarea())
    # TODO:albertas:2011-09-04: could not find max length of couchdb _id.
    doc_id = forms.CharField(max_length=255, widget=forms.HiddenInput())

    def __init__(self, document=None, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        if document and 'summary' in dict(document.items()):
            self.fields['summary'] = forms.CharField(initial=document['summary'],
                                                     widget=forms.widgets.Textarea())
