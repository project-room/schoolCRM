from django.views.generic.base import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.

class CourseIndexView(LoginRequiredMixin, View):
    login_url = '/log_in/'
    redirect_field_name = 'next'

    def get(self, request):

        return render(request, "lesson/lesson.html")