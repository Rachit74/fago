from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateCommunityForm
from .models import Community
from django.http import HttpResponseForbidden

# Create your views here.
def explore(request):
    communities = Community.objects.all()
    context = {
        'communities': communities
    }

    return render(request, 'communities/explore.html', context=context)

# view community method (one particular community)
def community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    posts = community.posts.all()
    members = community.members.all()

    context = {
        'community': community,
        'members': members,
        'posts': posts,
    }

    return render(request, 'communities/community.html', context=context)

@login_required
def create_community(request):
    user = request.user
    if request.method == "POST":
        form = CreateCommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.owner = user
            community.save()
            community.members.add(user)
            community.save()

            messages.success(request, "Your community has been created!")
            return redirect('community', community_id=community.id)
    else:
        form = CreateCommunityForm()

    context = {
        'form':form
    }

    return render(request, 'communities/create_com.html', context=context)

@login_required
def join_community(request, community_id):
    user = request.user
    community = get_object_or_404(Community, id=community_id)
    community.members.add(user)
    community.save()

    messages.success(request, f"You have joined {community.name}!")
    return redirect('community', community_id=community.id)

@login_required
def leave_community(request, community_id):
    user = request.user
    community = get_object_or_404(Community, id=community_id)
    community.members.remove(user)
    community.save()

    messages.warning(request, f"You left {community.name}!")
    return redirect('community', community_id=community.id)

@login_required
def delete_community(request, community_id):
    user = request.user
    community = get_object_or_404(Community, id=community_id)
    community_name = community.name

    if not user == community.owner:
        return HttpResponseForbidden("Forbidden")
    else:
        community.delete()

    messages.warning(request, f'Your community {community_name} was deleted!')
    return redirect('explore-communities')