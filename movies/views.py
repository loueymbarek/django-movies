from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Movie, Genre
from .forms import MovieForm, ReviewForm

def movie_list(request):
    genre_id = request.GET.get('genre')
    name_query = request.GET.get('name', '')
    min_rating = request.GET.get('min_rating', '')

    movies = Movie.objects.all()
    if genre_id:
        movies = movies.filter(genres__id=genre_id)
    if name_query:
        movies = movies.filter(title__icontains=name_query)
    if min_rating:
        try:
            min_rating = float(min_rating)
            # Filter movies by average_rating >= min_rating
            movies = [m for m in movies if m.average_rating() >= min_rating]
        except ValueError:
            pass
    genres = Genre.objects.all()
    # Get selected genres as a list of strings for template
    selected_genres = request.GET.getlist('genre')
    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'genres': genres,
        'request': request,
        'name_query': name_query,
        'min_rating': min_rating,
        'selected_genres': selected_genres,
    })

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    review_form = ReviewForm()
    return render(request, 'movies/movie_detail.html', {'movie': movie, 'review_form': review_form})

def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movies:movie_list')
    else:
        form = MovieForm()
    return render(request, 'movies/movie_form.html', {'form': form, 'title': 'Add Movie'})

def movie_edit(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:movie_detail', pk=pk)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'movies/movie_form.html', {'form': form, 'title': 'Edit Movie'})

def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('movies:movie_list')
    return render(request, 'movies/movie_confirm_delete.html', {'movie': movie})

def review_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('movies:movie_detail', pk=movie_pk)
        else:
            messages.error(request, 'There was a problem with your review. Please correct the errors below.')
            # Render the detail page with the invalid form (shows errors)
            return render(request, 'movies/movie_detail.html', {
                'movie': movie,
                'review_form': form,
            })
    return redirect('movies:movie_detail', pk=movie_pk)

def review_edit(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(movie.reviews, pk=review_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully!')
            return redirect('movies:movie_detail', pk=movie_pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'movies/review_form.html', {'form': form, 'movie': movie, 'review': review})

def review_delete(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(movie.reviews, pk=review_pk)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully!')
        return redirect('movies:movie_detail', pk=movie_pk)
    return render(request, 'movies/review_confirm_delete.html', {'movie': movie, 'review': review})