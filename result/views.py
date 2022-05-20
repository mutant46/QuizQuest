from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from .models import Result
from quiz.models import Quiz


class ResultView(View, LoginRequiredMixin):
    template_name = 'result/result.html'

    def get_queryset(self):
        q = get_object_or_404(
            Quiz, pk=self.kwargs['pk'], slug=self.kwargs['slug'])
        return Result.objects.get(quiz=q, user=self.request.user)

    def get(self, request, *args, **kwargs):
        result = self.get_queryset()
        return render(request, self.template_name, {'quiz_result': result})
