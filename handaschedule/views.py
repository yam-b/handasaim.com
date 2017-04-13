from django.shortcuts import render

def post_list(request):
    return render(request, 'handaschedule/post_list.html', {})