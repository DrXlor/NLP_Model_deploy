from django.db import models


class PredResults(models.Model):

    review = models.CharField(max_length=2000)
    tone_classification = models.CharField(max_length=30)
    score_classification = models.CharField(max_length=30)

    def __str__(self):
        return self.tone_classification, self.score_classification
