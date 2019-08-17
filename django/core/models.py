from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.db.models.aggregates import Sum
from django.conf import settings

from uuid import uuid4


def movie_directory_path_with_uuid(instance, filename):
    return "{}/{}".format(instance.movie_id, uuid4())


class MovieImage(models.Model):
    image = models.ImageField(upload_to=movie_directory_path_with_uuid)
    uploaded = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


class MovieManager(models.Manager):
    """
        Make smarter request to avoid hiting the
        database for each related item
    """

    def all_related_persons(self):
        qs = self.get_queryset()
        qs = qs.select_related('director')
        qs = qs.prefetch_related('writers', 'actors')
        return qs

    def all_related_persons_and_score(self):
        qs = self.all_related_persons()
        qs = qs.annotate(score=Sum('vote__value'))
        return qs


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

    director = models.ForeignKey(to='Person',
                                 on_delete=models.SET_NULL,
                                 related_name='directed',
                                 null=True, blank=True)

    writers = models.ManyToManyField(to='person',
                                     related_name='writing_credits',
                                     blank=True)

    actors = models.ManyToManyField(to='Person',
                                    through='Role',
                                    related_name='acting_credits',
                                    blank=True)

    # Replace the default object manager by MovieManager
    objects = MovieManager()

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
        return "{} ({})".format(
            self.title, self.year()
        )


class PersonManager(models.Manager):
    """
        Make smarter request to avoid hiting the
        database for each related item
    """

    def all_prefetched_movies(self):
        qs = self.get_queryset()
        return qs.prefetch_related(
            'directed',
            'writing_credits',
            'role_set__movie'
        )


class Person(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    born = models.DateField()
    died = models.DateField(blank=True, null=True)

    # Replace the default object manager by PersonManager
    objects = PersonManager()

    class Meta:
        ordering = ('last_name', 'first_name')

    def __str__(self):
        if self.died:
            return "{}, {} ({}-{})".format(
                self.last_name,
                self.first_name,
                self.born,
                self.died
            )

        return "{}, {} ({})".format(
            self.last_name,
            self.first_name,
            self.born
        )


class Role(models.Model):
    """
        The intermediary (join table) between
        Movie and Person
    """

    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=150)

    class Meta:
        unique_together = (
            'movie',
            'person',
            'name'
        )

    def __str__(self):
        return "{} {} {}".format(
            self.movie.id, self.person.id, self.name
        )


class VoteManager(models.Manager):
    """
        Check if a user model has a related Vote model
        instance for a given Movie model instance.
        If not, it will return a unsaved blank Vote object
    """

    def get_vote_or_unsaved_blank_vote(self, user, movie):
        try:
            return Vote.objects.get(
                user=user, movie=movie
            )
        except Vote.DoesNotExist:
            # Return an usaved (Created by the object constructor)
            # blank Vote instance
            return Vote(user=user, movie=movie)


class Vote(models.Model):

    UP = 1
    DOWN = -1
    VALUE_CHOICES = (
        (UP, "👍"),
        (DOWN, "👎"),
    )

    value = models.SmallIntegerField(choices=VALUE_CHOICES, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    voted_on = models.DateField(auto_now=True)

    # Replace the default manager by our custom manager
    objects = VoteManager()

    class Meta:
        unique_together = ('user', 'movie')
