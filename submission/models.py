from django.db import models


class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    problem_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    verdict = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'submission'


class Test(models.Model):
    id = models.IntegerField(primary_key=True)
    input = models.CharField(max_length=255, blank=True, null=True)
    output = models.CharField(max_length=255, blank=True, null=True)
    problem_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test'
