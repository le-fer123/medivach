from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView, ListView

from .models import Thread
from .services import parsethread, recursive

class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'thread_detail.html'

class ThreadListView(ListView):
    model = Thread
    template_name = 'thread_list.html'

def redirect_thread(request):
    return redirect(reverse('down'))


@csrf_exempt
def down_thread(request):
    if request.method == 'POST':
        url = request.POST['url']
        print(url)

        imglife, imghk = parsethread(url)
        print(imglife, imghk)
        thread = Thread.objects.create(title=url.split('/')[-1])

        lost = recursive(imglife, imghk, thread)
        print(lost)

        return redirect(reverse('thread_detail', kwargs={'pk': thread.pk}), context={"lost": lost})

    if request.method == 'GET':
        return render(request, 'down_thread.html')

