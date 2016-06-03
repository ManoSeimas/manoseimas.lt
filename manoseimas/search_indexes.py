from haystack import indexes

from manoseimas.mps_v2.models import ParliamentMember


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return ParliamentMember

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
