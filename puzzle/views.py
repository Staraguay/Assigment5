from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from puzzle.form import PuzzleForm
import binascii
import math
import random

# Create your views here.
def treasure_hunt(number):

    attempt = 0
    previous_numbers = set()
    steps = ''
    while attempt < 5:

        guess_number = random.randint(1, 100)

        if guess_number in previous_numbers:
            continue
        previous_numbers.add(guess_number)

        steps += 'Step {}: Try with the number: {}\n'.format(attempt+1, guess_number)
        if guess_number == number:
            return {'result':True, 'steps':steps}
        else:
            if attempt == 4:
                return {'result':False, 'steps':steps}
        attempt += 1

class PuzzleHome(TemplateView):
    template_name = 'home.html'
    form_class = PuzzleForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']
            message = form.cleaned_data['text']

            respond = {}

            # even/odd check
            num = int(number)
            if (num % 2) == 0:
                # even
                square_number = math.sqrt(num)
                respond['nPuzzle'] = int(square_number)

            else:
                # odd
                cube_number = pow(num, 3)
                respond['nPuzzle'] = cube_number

            # Text Puzzle
            bmessage = bin(int(binascii.hexlify(message.encode()), 16))[2:]
            vocals_count = sum(v in {"a", "A", "e", "E", "i", "I", "o", "O", "u", "U"} for v in message)

            respond['bmessage'] = bmessage
            respond['vocals'] = vocals_count
            respond['treasure'] = treasure_hunt(num)

        return render(request, self.template_name, {'result': respond, 'form': form})