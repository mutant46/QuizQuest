from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from .models import Result
from question.models import Question
import random
from quiz.models import Quiz
from django.http import JsonResponse
import xlwt
from django.http import HttpResponse


class TestData(LoginRequiredMixin, View):
    '''
    Preparing and sending Question & Answers as json for
    Quiz.slug = slug
    '''

    def get(self, request, *args, **kwargs):
        quiz = get_object_or_404(
            Quiz, slug=kwargs.get('slug'), pk=kwargs.get('pk'))
        questions = []
        for q in quiz.get_questions():
            questions.append({str(q): [a.text for a in q.get_answers()]})
        random.shuffle(questions)
        return JsonResponse({
            'data': questions,
            'time': quiz.time
        })


class CalcTestData(View, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        '''
        Handling Test data from Ajax , Calculate and return results
        '''

        def handle_result(user, quiz, score):
            '''
            Create or update the results for the user
            with this quiz
            '''
            score = score / quiz.total_questions() * 100
            status = 'Pass' if score >= quiz.percentage else 'Fail'
            try:
                Result.objects.get(user=user, quiz=quiz)
            except Result.DoesNotExist:
                print("this is not working")
                Result.objects.create(user=user, quiz=quiz,
                                      percentage=score, status=status).save()
            else:
                print('this is working')
                obj = Result.objects.get(user=user, quiz=quiz)
                obj.percentage = score
                obj.status = status
                obj.save()

        def prepare_result_list(data, quiz):
            '''
            Comparing User Test data with actual answers 
            & returning result_list
            '''
            result_list = []
            score = 0
            data.pop('csrfmiddlewaretoken')
            for k in data.keys():
                q = Question.objects.get(text=k, quiz=quiz)
                ans = q.get_correct_ans().text
                if data[q.text][0] != '':
                    if data[q.text][0] == ans:
                        score += 1
                    result_list.append(
                        {str(q): {'correct_answer': ans, 'answerd': data[q.text][0]}})
                else:
                    result_list.append({q.text: "not answered"})
            return score, result_list

        if request.is_ajax():
            quiz = Quiz.objects.get(
                slug=kwargs.get('slug'), pk=kwargs.get('pk'))
            data = dict(request.POST.lists())
            score, result_list = prepare_result_list(data, quiz)
            handle_result(request.user, quiz, score)

            popularity = request.session.get('submission', True)
            if popularity:
                quiz.papularity += 1
                request.session['submission'] = False
                quiz.save()

        return JsonResponse({
            'results': result_list,
        })


class ResultView(View, LoginRequiredMixin):
    template_name = 'result/result.html'

    def get_queryset(self):
        q = get_object_or_404(
            Quiz, pk=self.kwargs['pk'], slug=self.kwargs['slug'])
        return Result.objects.get(quiz=q, user=self.request.user)

    def get(self, request, *args, **kwargs):
        result = self.get_queryset()
        return render(request, self.template_name, {'quiz_result': result})


class EXportResultsView(LoginRequiredMixin, View):
    reponse = HttpResponse(content_type='application/ms-excel')
    reponse['Content-Disposition'] = 'attachment; filename="results.xls"'

    def get(self, request, *args, **kwargs):
        quiz = Quiz.objects.get(id=self.kwargs['pk'])
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Results-%s' % quiz.name)

        # font style for header row
        header_style = xlwt.XFStyle()
        header_style.font.bold = True

        columns = ['Username', 'Email', 'Percentage', 'status']

        for col, header in enumerate(columns):
            ws.write(0, col, header, header_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = Result.objects.filter(quiz_id=quiz.id)
        for row, result in enumerate(rows):
            ws.write(row + 1, 0, result.user.username, font_style)
            ws.write(row + 1, 1, result.user.email, font_style)
            ws.write(row + 1, 2, result.percentage, font_style)
            ws.write(row + 1, 3, result.status, font_style)

        wb.save(self.reponse)
        return self.reponse
