from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class ResultView(View, LoginRequiredMixin):
    '''
    veiw for that test page
    '''
    def get(self, request, *args, **kwargs):
        x = request.session.get('quiz_result_list')
        print(type(x))
        context = {
            'result_list' : list(request.session.get('quiz_result_list'))
        }
        return render(request, 'result/result.html', context)
