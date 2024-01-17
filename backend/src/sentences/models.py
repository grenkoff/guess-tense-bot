from django.db import models

class Sentences(models.Model):

    TENSES = [
        ('present_simple', 'Present Simple'),
        ('present_continuous', 'Present Continuous'),
        ('present_perfect', 'Present Perfect'),
        ('present_perfect_continuous', 'Present Perfect Continuous'),
        ('past_simple', 'Past Simple'),
        ('past_continuous', 'Past Continuous'),
        ('past_perfect', 'Past Perfect'),
        ('past_perfect_continuous', 'Past Perfect Continuous'),
        ('future_simple', 'Future Simple'),
        ('future_continuous', 'Future Continuous'),
        ('future_perfect', 'Future Perfect'),
        ('future_perfect_continuous', 'Future Perfect Continuous'),
        ('future_simple_in_the_past', 'Future Simple in the Past'),
        ('future_continuous_in_the_past', 'Future Continuous in the Past'),
        ('future_perfect_in_the_past', 'Future Perfect in the Past'),
        ('future_perfect_continuous_in_the_past', 'Future Perfect Continuous in the Past'),
    ]

    sentence = models.CharField(verbose_name="Sentence", max_length=300)
    tense = models.CharField(verbose_name="Tense", max_length=37, choices=TENSES)

    def __str__(self):
        return self.tense + " " + self.sentence