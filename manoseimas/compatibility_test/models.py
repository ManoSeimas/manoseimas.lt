from django.db import models


class CompatTest(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()


class TestGroup(models.Model):
    name = models.CharField(max_length=200)


class PoliticalTopic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    mp_positions = models.TextField(blank=True, null=True) # JSON-serialized (text) [{mp_id, fraction_id, pozicija}], recalculating on each voting adding
    test = models.ForeignKey(CompatTest, on_delete=models.CASCADE)
    group = models.ForeignKey(TestGroup)

    def votings(self):
        return self.voting_set.objects.all()


class Voting(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    source = models.URLField()
    factor = models.PositiveIntegerField(default=1)  # voting importance
    topic = models.ForeignKey(PoliticalTopic)


class Argument(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    supporting = models.BooleanField(default=True)
    topic = models.ForeignKey(PoliticalTopic, on_delete=models.CASCADE)
