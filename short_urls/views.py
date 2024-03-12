from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from .models import ShortURL
from .forms import ShortURLForm

# Retrieve the ShortURL object associated with the provided short_code and redirect to the original url if found.
def redirect_to_original_url(request, short_code):
    try:
        short_url = ShortURL.objects.get(short_code=short_code)
    except ShortURL.DoesNotExist:
        # Handle case where short_code is not found
        return HttpResponseNotFound("Short URL not found")

    return redirect(short_url.original_url)


# List all short_urls for the authenticated user
def short_url_list(request):
    short_urls = ShortURL.objects.filter(user=request.user)
    return render(request, 'short_urls/list.html', {'short_urls': short_urls})

# Create a short_url
def short_url_create(request):
    if request.method == 'POST':
        form = ShortURLForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('short_url_list')
    else:
        form = ShortURLForm()
    return render(request, 'short_urls/create.html', {'form': form})

# Update a short_url
def short_url_update(request, pk):
    # Return a 404 if the object doesn't exist or isn't associated to the authenticated user
    short_url = get_object_or_404(ShortURL, pk=pk, user_id=request.user.id)
    if request.method == 'POST':
        form = ShortURLForm(request.POST, instance=short_url)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('short_url_list')
    else:
        form = ShortURLForm(instance=short_url)
    return render(request, 'short_urls/update.html', {'form': form})

# Delete a short_url
def short_url_delete(request, pk):
    # Return a 404 if the object doesn't exist or isn't associated to the authenticated user
    try:
        short_url = ShortURL.objects.get(pk=pk, user_id=request.user.id)
    except ShortURL.DoesNotExist:
        # TODO: Add logging here for unexpected cases: when a user deletes a deleted object or attempts to delete another user's object
        return redirect('short_url_list')
    
    if request.method == 'POST':
        short_url.delete()
        return redirect('short_url_list')
    return render(request, 'short_urls/delete.html', {'short_url': short_url})
