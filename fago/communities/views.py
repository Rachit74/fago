from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateCommunityForm
from .models import Community
from django.http import HttpResponse, HttpResponseForbidden
from posts.models import Post

from django.contrib.auth.models import User

from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

class ExploreView(ListView):
    """
    List View used to simply show a list of objects
    takes the following
    model_name, template_name, context_name
    for more: https://docs.djangoproject.com/en/5.1/ref/class-based-views/generic-display/#listview
    """
    model = Community
    template_name = 'communities/explore.html'
    context_object_name = 'communities'

class CommunityView(DetailView):
    model = Community
    template_name = 'communities/community.html'
    context_object_name = 'community'
    slug_field = 'name'
    slug_url_kwarg = 'community'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        community = self.object
        context['posts'] = community.posts.filter(pinned=False).all()
        context['pinned_posts'] = community.posts.filter(pinned=True).all()
        context['members'] = community.members.all()

        return context


@login_required
def create_community(request):
    if request.method == "POST":
        form = CreateCommunityForm(request.POST)
        community = form.save(commit=False)
        community.owner = request.user
        community.save()
        community.members.add(request.user)

        messages.success(request, "Your community was created!")
        return redirect('community', community=community.name)
    else:
        form = CreateCommunityForm()
    
    context = {
        'form' : form
    }

    return render(request, 'communities/create_com.html', context=context)

@login_required
def join_community(request, community):
    user = request.user
    community = get_object_or_404(Community, name=community)
    community.members.add(user)
    community.save()

    messages.success(request, f"You have joined {community.name}!")
    return redirect('community', community=community.name)

@login_required
def leave_community(request, community):
    user = request.user
    community = get_object_or_404(Community, name=community)
    if user == community.owner:
        messages.error(request, "You can not leave the community as the owner!")
        return redirect('community', community=community.name)
        
    community.members.remove(user)
    community.save()

    messages.warning(request, f"You left {community.name}!")
    return redirect('community', community=community.name)

@login_required
def delete_community(request, community):
    user = request.user
    community = get_object_or_404(Community, name=community)
    community_name = community.name

    if not user == community.owner:
        return HttpResponseForbidden("Forbidden")
    else:
        community.delete()

    messages.warning(request, f'Your community {community_name} was deleted!')
    return redirect('explore-communities')

# Pin post view
@login_required
def pin_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    community = post.community

    if not user == community.owner:
        return HttpResponseForbidden("Forbidden")
    
    post.pinned = True
    post.save()
    messages.success(request, "Post was pinned")
    return redirect('community', community=community.name)

# Unpin post view
@login_required
def unpin_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    community = post.community

    if not user == community.owner:
        return HttpResponseForbidden("Forbidden")
    
    post.pinned = False
    post.save()
    messages.success(request, "Post was unpinned")
    return redirect('community', community=community.name)

# Community Admin Views

@login_required
def dashboard(request, community):
    community = get_object_or_404(Community, name=community)

    if not community.owner == request.user:
        return HttpResponseForbidden("Forbidden")
    
    members = community.members.all()
    
    context = {
        'community': community,
        'members': members,
    }

    return render(request, 'communities/dashboard.html', context=context)

# Community admin kick member
@login_required
def admin_kick(request, community, member_id):
    user = request.user
    community = get_object_or_404(Community, name=community)
    member = get_object_or_404(User, id=member_id)

    if not user == community.owner:
        return HttpResponseForbidden("Forbidden")
    
    """
    This login prevents the community owner from kicking himself out of the community!
    if the member that is being kicked is the owner of the community that prevent the kick.
    """
    if member == community.owner:
        messages.error(request, "Can not kick yourself from your own community!")
        return redirect('dashboard', community=community)

    community.members.remove(member)

    messages.success(request, f"{member} was kicked from {community}")
    return redirect('dashboard', community=community)