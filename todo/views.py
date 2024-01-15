from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse

import json

from .models import Task
from .forms import TaskForm
# Create your views here.
def is_ajax(request):
        return request.headers.get('x-requested-with') == 'XMLHttpRequest'

class TaskList(ListView):

    model = Task
    template_name = 'tasks.html'
    ordering = ['status', 'start_date']
    context_object_name = 'tasks'


class TaskCreate(CreateView):

    model = Task
    success_url = reverse_lazy('todo:tasks')
    template_name = 'form.html'
    form_class = TaskForm

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            form = self.get_form()
            if form.is_valid():
                instance = form.save()
                data = {'success': True, 'data': instance.get_all_values_to_dict()}
                status_code = 200
            else:
                data = {'success': False, 'errors': form.errors}
                status_code = 409
            return JsonResponse(data=data, status=status_code)
        else:
            return super().post(request, *args, **kwargs)
  

class TaskDelete(DeleteView):

    model = Task
    success_url = reverse_lazy('todo:tasks')
    template_name = 'confirm_delete.html'

    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse(data={'success': True})
        else:
            return super().post(request, *args, **kwargs)
        
    
class TaskUpdate(UpdateView):

    model = Task
    form_class = TaskForm
    template_name = 'form.html' 
    success_url = reverse_lazy('todo:tasks')

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk and is_ajax(request):
            self.object = self.get_object() 
            form = self.form_class(request.POST, instance=self.object)
            if form.is_valid():
                # Manually compare the initial data with the submitted data
                initial_data = {k: v for k, v in form.initial.items() if k in form.data}
                submitted_data = {k: v for k, v in form.cleaned_data.items() if k in form.data}
                if initial_data == submitted_data:
                    data = {'success': False, 'errors': {'form': 'Your form has not changed.'}}
                    status_code = 409
                else:
                    instance = form.save()
                    data = {'success': True, 'data': instance.get_all_values_to_dict()}
                    status_code = 200
            else:
                data = {'success': False, 'errors': form.errors}
                status_code = 409
        elif pk is None:
            data = {'success': False, 'errors': {'pk': 'Primary key not provided.'}}
        else: 
            return super().post(request, *args, **kwargs)
        return JsonResponse(data=data, status=status_code) 
    

#Search todolist use Django ORM