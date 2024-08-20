from django.shortcuts import render


#posts dummy data
posts = [
    {
        'id':1,
        'title': 'The Post',
        'content': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Pariatur exercitationem fuga iusto quis illo corrupti hic ullam doloribus deserunt nisi maxime porro ipsam, eligendi facilis incidunt! Libero cum aperiam dolores.',
    },
        {
        'id':2,
        'title': 'The Post',
        'content': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Pariatur exercitationem fuga iusto quis illo corrupti hic ullam doloribus deserunt nisi maxime porro ipsam, eligendi facilis incidunt! Libero cum aperiam dolores.',
    },
        {
        'id':3,
        'title': 'The Post',
        'content': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Pariatur exercitationem fuga iusto quis illo corrupti hic ullam doloribus deserunt nisi maxime porro ipsam, eligendi facilis incidunt! Libero cum aperiam dolores.',
    },
]

# Create your views here.
def home(request):
    context = {
        'posts': posts
    }
    return render(request, "posts/index.html", context=context)