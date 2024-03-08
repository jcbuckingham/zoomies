from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from .models import ShortURL
from .forms import ShortURLForm

def redirect_to_original_url(request, short_code):
    # Retrieve the ShortURL object associated with the provided short_code
    try:
        short_url = ShortURL.objects.get(short_code=short_code)
    except ShortURL.DoesNotExist:
        # Handle case where short_code is not found
        return HttpResponseNotFound("Short URL not found")

    # Redirect to the original URL
    return redirect(short_url.original_url)


# List all short_urls
def short_url_list(request):
    short_urls = ShortURL.objects.all()
    return render(request, 'short_urls/list.html', {'short_urls': short_urls})

# Create a short_url
def short_url_create(request):
    if request.method == 'POST':
        form = ShortURLForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('short_url_list')
    else:
        form = ShortURLForm()
    return render(request, 'short_urls/create.html', {'form': form})

# Details for a short_url
def short_url_detail(request, pk):
    short_url = get_object_or_404(ShortURL, pk=pk)
    return render(request, 'short_urls/detail.html', {'short_url': short_url})

# Update a short_url
def short_url_update(request, pk):
    short_url = get_object_or_404(ShortURL, pk=pk)
    if request.method == 'POST':
        form = ShortURLForm(request.POST, instance=short_url)
        if form.is_valid():
            form.save()
            return redirect('short_url_list')
    else:
        form = ShortURLForm(instance=short_url)
    return render(request, 'short_urls/update.html', {'form': form})

# Delete a short_url
def short_url_delete(request, pk):
    print("%^%^%^%^%^%^%^%^%^%^%")
    short_url = get_object_or_404(ShortURL, pk=pk)
    if request.method == 'POST':
        print("DELETING....")
        short_url.delete()
        return redirect('short_url_list')
    print("DID NOT DELETE")
    return render(request, 'short_urls/delete.html', {'short_url': short_url})
