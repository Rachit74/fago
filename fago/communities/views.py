from django.shortcuts import render

c = [
    {
        'id':1,
        'name': 'name',
        'desc': 'desc',
    },
        {
        'id':2,
        'name': 'name',
        'desc': 'desc',
    },
        {
        'id':2,
        'name': 'name',
        'desc': 'desc',
    },
]

# Create your views here.
def explore(request):

    context = {
        'communities': c
    }

    return render(request, 'communities/explore.html', context=context)