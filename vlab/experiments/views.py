from django.shortcuts import render

# Create your views here.

def experiment(request, exp, stage):
	template = exp + '/' + stage + '.html'
	return render(request, template, {})
