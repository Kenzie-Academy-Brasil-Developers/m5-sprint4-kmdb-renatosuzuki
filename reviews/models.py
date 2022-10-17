from django.db import models


class RecomendationChoice(models.TextChoices):
    MUST = "Must Watch"
    SHOULD = "Should Watch"
    AVOID = "Avoid Watch"
    NO_OPINION = "No Opinion"


class Review(models.Model):
    stars = models.IntegerField()
    review = models.TextField()
    spoilers = models.BooleanField(null=True, default=False)
    recomendation = models.CharField(max_length=50, choices=RecomendationChoice.choices, default=RecomendationChoice.NO_OPINION)

    critic_user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reviews")
    movie = models.ForeignKey("movies.Movie", on_delete=models.CASCADE, related_name="reviews")