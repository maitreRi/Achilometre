from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ChessRoomView(LoginRequiredMixin, TemplateView):
    template_name = 'chess_room/chess_room.html'
