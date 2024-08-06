from django.db import models


class Estudio(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Produtor(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Filme(models.Model):
    year = models.IntegerField(db_index=True)
    title = models.CharField(max_length=255, unique=True, db_index=True)
    studios = models.ManyToManyField(Estudio)
    producers = models.ManyToManyField(Produtor)
    winner = models.CharField(max_length=10, db_index=True)

    def __str__(self):
        return self.title
