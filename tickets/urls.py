from django.urls import path

from .views import (AllTicketsAdmin, AllTicketsUser, DetailTicketsAdmin,
                    SendTicket, CheckAnswerUser, SendAnswerUser)

urlpatterns = [
    path('send', SendTicket.as_view()),
    path('chek_ticket_user', AllTicketsUser.as_view()),
    path('chek_ticket_answer_user', CheckAnswerUser.as_view()),
    path('chek_ticket_answer_user/<int:pk>', SendAnswerUser.as_view()),
    path('check_tickets_admin', AllTicketsAdmin.as_view()),
    path('check_tickets_admin/<int:pk>', DetailTicketsAdmin.as_view()),
    # path('send_answer_admin', SendTicketsAnswerAdmin.as_view()),
]
