from django.urls import path
from calculator.views import calculate,get_history,delete_history,delete_all_history
urlpatterns = [
    path('calculate/', calculate, name="calculate"),
    path('calculate/history/', get_history, name='get_history'),
    path('calculate/history/<int:id>/', delete_history, name='delete_history'),
    path('calculate/delete_all_history/', delete_all_history, name='delete_all_history'),
]
