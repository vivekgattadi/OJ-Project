from re import I
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
# Create your views here.
from .models import Problem, Solution, TestCase

from django.urls import reverse
from django.utils import timezone
from django.views import generic
import os, filecmp

from django.contrib.auth.decorators import login_required
import tempfile

def index(request):
    return HttpResponse("Hello World. You are at the judge index.")

@login_required
def ListProblems(request):
    latest_question_list = Problem.objects.order_by('difficulty')[:10]
    #output = "\n".join([q.statement for q in latest_question_list])
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'judge/ListProblems.html', context)

@login_required
def ShowindividualProblem(request, question_id):
    question = get_object_or_404(Problem, pk=question_id)
    return render(request, 'judge/ShowindividualProblem.html', {'question':question})

@login_required
def CodeSubmission(request, question_id):

    # f = request.FILES['solution']
    # with open('/Users/vivekgattadi/Algo-Project/solution.cpp', 'wb+') as dest:
    #     for chunk in f.chunks():
    #         dest.write(chunk)
        
    # sol = open('/Users/vivekgattadi/Algo-Project/solution.cpp', "r")
    # os.system('g++ /Users/vivekgattadi/Algo-Project/solution.cpp')
    # os.system('./a.out < /Users/vivekgattadi/Algo-Project/inp.txt > /Users/vivekgattadi/Algo-Project/out.txt')

    # out1 = '/Users/vivekgattadi/Algo-Project/out.txt'
    # out2 = '/Users/vivekgattadi/Algo-Project/actual_out.txt'


    # if(filecmp.cmp(out1, out2, shallow=False)):
    #     verdict = 'Accepted'
    # else:
    #     verdict = 'Wrong Answer'

    codeText = request.POST.get('textsolution')
    lang = request.POST.get('language')
    print(lang)
    tempSolutioncpp = tempfile.NamedTemporaryFile(suffix=".cpp")
    tempSolutionpy = tempfile.NamedTemporaryFile(suffix=".py")

    if (lang == "cpp"):
        tempSolutioncpp.write(str.encode(codeText))
        tempSolutioncpp.seek(0)
        tempSolutionpy.close()
    elif (lang == "python"):
        tempSolutionpy.write(str.encode(codeText))
        tempSolutionpy.seek(0)
        tempSolutioncpp.close()

    problem = get_object_or_404(Problem, pk=question_id)

    inp = problem.testcase_set.all()

    if (lang == "cpp"):
        os.system('g++ ' + tempSolutioncpp.name)

    verdict = 'Accepted'
    for i in inp:
        tempOutput = tempfile.NamedTemporaryFile(suffix=".txt")
        tempOutput.seek(0)

        tempInput = tempfile.NamedTemporaryFile(suffix=".txt")
        tempInput.write(str.encode(i.input_test))

        tempInput.seek(0)
        if (lang == "cpp"):
            os.system('./a.out < ' + tempInput.name + ' > ' + tempOutput.name)
        elif (lang == "python"):
            os.system('python ' + tempSolutionpy.name + ' < ' + tempInput.name + ' > ' + tempOutput.name)

        tempActualOutput = tempfile.NamedTemporaryFile(suffix=".txt")
        tempActualOutput.write(str.encode(i.output_test))

        tempOutput.seek(0)
        tempActualOutput.seek(0)

        tempOutputStr = tempOutput.read().decode("utf-8")
        tempActualOutputStr = ""
        count = 0
        with open(tempActualOutput.name, 'r') as var:
            for line in var:
                count = count+1
                line = line.replace('\r', '')
                tempActualOutputStr = tempActualOutputStr + line
        
        # print(tempActualOutputStr)
        # print(tempOutputStr)

        if(tempActualOutputStr.strip() == tempOutputStr.strip()):
            verdict = 'Accepted'
        else:
            verdict = 'Wrong Answer'
            break

        tempOutput.close()
        tempActualOutput.close()
        tempInput.close()
    
    if (lang == "cpp"):
        tempSolutioncpp.close()
    elif (lang == "python"):
        tempSolutionpy.close()


    solution = Solution()###
    solution.problem = Problem.objects.get(pk=question_id)
    solution.verdict = verdict
    solution.submitted_at = timezone.now()
    solution.submitted_code = codeText 
    solution.save()

    return redirect('judge:Leaderboard')

@login_required
def Leaderboard(request):
    solutions = Solution.objects.all().order_by('-submitted_at')
    return render(request, 'judge/Leaderboard.html', {'solutions':solutions})



