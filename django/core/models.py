from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify


class Movie(models.Model):
    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3

    RATING = (
        (NOT_RATED, 'NR - Not Rated'),
        (RATED_G, 'G - General Audiances'),
        (RATED_PG, 'PG - Parental Guidance Suggested'),
        (RATED_R, 'R - Restricted'),
    )

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150,
                            unique_for_date='released')
    description = models.TextField()
    released = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(choices=RATING, default=NOT_RATED)
    runtime = models.PositiveIntegerField()
    website = models.URLField(blank=True)

    class Meta:
        ordering = ('-released', 'title')

    # Canonical urls
    def get_absolute_url(self):
        return reverse('core:movie_detail',
                       kwargs={'pk': self.id})

    # Autofill the slug field with the title before save
    def save(self, *args, **kwargs):
        self.url = slugify(self.title)
        super(Movie, self).save(*args, **kwargs)

    def year(self):
        """Return the year of the first release"""
        return self.released.strftime('%Y')

    def __str__(self):
        return f"{self.title} ({self.year()})"
