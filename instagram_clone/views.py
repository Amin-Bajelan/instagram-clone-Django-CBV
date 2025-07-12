from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'instagram_clone/index.html'
