from django.shortcuts import render,render_to_response
from django.http import *

def modifyTerm(request):
    return render_to_response('jiaowu_term.html')