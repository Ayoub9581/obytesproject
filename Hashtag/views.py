from django.shortcuts import render
from django.views.generic import ListView
from django.http import Http404
from .models import Hashtag


class HashtagStatusListView(ListView):
    model = Hashtag
    template_name = 'status/all_hashtag_status.html'

    def get_queryset(self):
        qs = Hashtag.objects.get(tag=self.kwargs['hashtag'])
        if qs is None:
            return Http404
        qs = qs.get_messages()
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.kwargs['hashtag']
        return context


def get_all_hashtag(request):
    query = request.GET.get('q')
    context = {}
    if query is not None and query != "":
        print(query)
        qs = Hashtag.objects.filter(tag__startswith=query)
        context['object_list'] = qs
    return render(request, 'hashtag/get_all_tags.html', context)
