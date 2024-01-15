from django.urls import path

from .views import TaskList, TaskCreate, TaskDelete, TaskUpdate

app_name = 'todo'

urlpatterns = [
    path('', view=TaskList.as_view(), name='tasks'),
    path('create/', view=TaskCreate.as_view(), name='create'),
    path('delete/<int:pk>', TaskDelete.as_view(), name='delete'),
    path('update/<int:pk>', TaskUpdate.as_view(), name='update'),
]

