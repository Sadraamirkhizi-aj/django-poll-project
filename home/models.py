from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    image = models.ImageField(upload_to='choices/', null=True, blank=True)
    is_pending = models.BooleanField(default=False, verbose_name='گزینه معلق')

    def __str__(self):
        return self.choice_text
