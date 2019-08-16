from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, )
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from core.models import Movie, Person, Vote
from core.forms import VoteForm


class MovieList(ListView):
    model = Movie
    # template_name can be omited see below
    template_name = 'core/movie_list.html'
    context_object_name = 'movies'
    paginate_by = 3


class MovieDetail(DetailView):
    queryset = Movie.objects.all_related_persons_and_score()
    # We can omit the template_name because django
    # search the associated template with this pattern
    # 'app_name/ModelName_detail.html'
    # template_name = 'core/movie_detail.html'

    def get_context_data(self, **kwargs):
        """
            Try to get the user's vote for the movie,
            instantiate the form and know which URL
            to submit the vote to (create_vote or
            update_vote)
        """

        cntx = super().get_context_data(**kwargs)
        # If the user is authenticated
        if self.request.user.is_authenticated:
            # Try to retrieve the vote
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(
                user=self.request.user,
                movie=self.object
            )

            # If vote already exist(the user has voted)
            # Then, it's a vote update
            if vote.id:
                vote_form_url = reverse(
                    'core:update_vote',
                    kwargs={
                        'movie_id': vote.movie.id,
                        'pk': vote.id
                    }
                )
            # It's the first time to vote the movie
            else:
                vote_form_url = reverse(
                    'core:create_vote',
                    kwargs={
                        'movie_id': self.object.id
                    }
                )

            # Create the vote form
            vote_form = VoteForm(instance=vote)
            # Fill the cntx variables
            cntx['vote_form'] = vote_form
            cntx['vote_form_url'] = vote_form_url

        return cntx


class PersonDetail(DetailView):
    # No need to add Model attribut because
    # it's automatically deduced from the queryset
    queryset = Person.objects.all_prefetched_movies()
    context_object_name = 'person'


class CreateVote(LoginRequiredMixin, CreateView):
    """
        Handle the logic for create a new vote
    """
    form_class = VoteForm

    def get_initial(self):
        """
            Take care for pre-populate the form with initial
            values before the form gets data values from
            the request
        """

        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial

    def get_success_url(self):
        """
            Return the success URL in the case where the form
            was successfuly submited
        """

        movie_id = self.object.movie.id
        return reverse('core:movie_detail', kwargs={
            'pk': movie_id})

    def render_to_response(self, context, **response_kwargs):
        """
            Return an URL in all others case where the
            form was not submited successfuly
        """

        movie_id = context['object'].id
        movie_detail_url = reverse('core:movie_detail', kwargs={
            'pk': movie_id
        })
        return redirect(to=movie_detail_url)


class UpdateVote(LoginRequiredMixin, UpdateView):
    """
        Handle the logic to update a vote
    """

    form_class = VoteForm
    queryset = Vote.objects.all()

    def get_object(self, queryset=None):
        """
            Check if the vote entered is for the logged'in user
            if not throws a PermissionDenied exception
        """

        vote = super().get_object(queryset)
        user = self.request.user

        if vote.user != user:
            raise(PermissionDenied,
                  'You\'re not authorized to vote for another user !')
        return vote

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('core:movie_detail',
                       kwargs={'pk': movie_id}
                       )

    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse('core:movie_detail', kwargs={
            'pk': movie_id
        })
        return redirect(to=movie_detail_url)
