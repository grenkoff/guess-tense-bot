from django.db import models

class Sentences(models.Model):

    TENSES = [
        ('Pr Si', 'Present Simple'),
        ('Pr Co', 'Present Continuous'),
        ('Pr Pe', 'Present Perfect'),
        ('Pr Pe Co', 'Present Perfect Continuous'),
        ('Pa Si', 'Past Simple'),
        ('Pa Co', 'Past Continuous'),
        ('Pa Pe', 'Past Perfect'),
        ('Pa Pe Co', 'Past Perfect Continuous'),
        ('Fu Si', 'Future Simple'),
        ('Fu Co', 'Future Continuous'),
        ('Fu Pe', 'Future Perfect'),
        ('Fu Pe Co', 'Future Perfect Continuous'),
    ]

    sentence = models.CharField(verbose_name="Sentence", max_length=300)
    tense = models.CharField(verbose_name="Tense", max_length=37, choices=TENSES)

    def __str__(self):
        return self.sentence + " -> " + self.tense