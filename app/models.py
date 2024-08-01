from django.db import models


class Filme(models.Model):
    """Modelo que representa um filme no banco de dados."""
    year = models.IntegerField(db_index=True)
    title = models.CharField(max_length=255, unique=True, db_index=True)
    studios = models.CharField(max_length=255, db_index=True)
    producers = models.CharField(max_length=255, db_index=True)
    winner = models.CharField(max_length=10, db_index=True)

    def __str__(self):
        return self.title
