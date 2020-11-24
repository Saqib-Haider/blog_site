from django.shortcuts import render, get_object_or_404,redirect
from django.http import Http404, HttpResponseRedirect,request
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from urllib.parse import quote_plus
from django.contrib.auth.decorators import login_required



# Create your views here.
def home(request):
    return render(request, "home.html")

def registration(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_url')

    return render(request, "register.html", {"form":form})

def create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Posted")
        return HttpResponseRedirect(instance.get_absolute_url())
    data = {
        "form": form,
    }
    return render(request, "form.html", data)


def detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    share_string = quote_plus(instance.content)
    data = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
    }
    return render(request,"detail.html", data)

@login_required
def list(request):
    queryset_list = Post.objects.all().order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all().order_by("-timestamp")
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(title__icontains=query)

    paginator = Paginator(queryset_list, 3)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    data = {
            "object_list": queryset,
            "title": "List",
            "page_request_var": page_request_var,
        }

    return render(request,"list.html",data)


def update(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Post Saved")
        return HttpResponseRedirect(instance.get_absolute_url())

    data = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "form.html", data)

def delete(resquest, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("list")


