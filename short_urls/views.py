from django.shortcuts import render, get_object_or_404, redirect
from .models import ShortURL
from .forms import ShortURLForm

def short_url_list(request):
    short_urls = ShortURL.objects.all()
    return render(request, 'short_urls/list.html', {'short_urls': short_urls})

def short_url_create(request):
    if request.method == 'POST':
        form = ShortURLForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('short_url_list')
    else:
        form = ShortURLForm()
    return render(request, 'short_urls/create.html', {'form': form})

def short_url_detail(request, pk):
    short_url = get_object_or_404(ShortURL, pk=pk)
    return render(request, 'short_urls/detail.html', {'short_url': short_url})

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

def short_url_delete(request, pk):
    short_url = get_object_or_404(ShortURL, pk=pk)
    if request.method == 'POST':
        short_url.delete()
        return redirect('short_url_list')
    return render(request, 'short_urls/delete.html', {'short_url': short_url})
