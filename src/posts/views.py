import urllib.parse
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.
from .models import Post
from .forms import PostForm
from PIL import Image
import glob,os
from django.utils import timezone
from django.db.models import Q
from comments.forms import CommentForm
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from .utils import get_read_time


def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form=PostForm(request.POST or None,request.FILES or None)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.user=request.user
		# image=Image.open(instance.image)
		# image.show()
		# image.thumbnail((400,400))
		# image.show()
		instance.save()
		messages.success(request,"Successfully Creates")
		return HttpResponseRedirect(instance.get_absolute_url())
	# else:
	# 	messages.error(request,"Server error Please try fter sometime")
	# if request.method=="POST":
	# 	print(request.POST)image
	
	context={
	"form":form
	}
	return render(request,"post_form.html",context)

def post_detail(request,id):
	instance=get_object_or_404(Post,id=id)	
	if instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string=urllib.parse.quote(instance.content)
	print(get_read_time(instance.content))# f,folder,folder1,image=instance.image.url.split("/")
	print(get_read_time(instance.get_markdown()))
	# print(image)
	# rel=".././media_cdn/"+folder1+"/"+image
	# print(rel)
	# image1=Image.open(rel)
	# image1.thumbnail((1000,1000))
	# image1.show()
	# name,ext=image.split(".")
	# image1.save(".././media_cdn/"+folder1+"/"+name,"JPEG")

	# content_type=ContentType.objects.get_for_model(Post)
	# obj_id=instance.id
	# comments=Comment.objects.filter(content_type=content_type,object_id=obj_id)
	initial_data={
		"content_type":instance.get_content_type,
		"object_id":instance.id
	}
	commentForm=CommentForm(request.POST or None,initial=initial_data)
	if commentForm.is_valid() and request.user.is_authenticated():
		# print(commentForm.cleaned_data)
		c_type=commentForm.cleaned_data.get("content_type")
		content_type=ContentType.objects.get(model=c_type)
		obj_id=commentForm.cleaned_data.get("object_id")
		content_data=commentForm.cleaned_data.get("content")
		parent_obj=None

		try:
			parent_id=int(request.POST.get("parent_id"))
		except:
			parent_id=None

		if parent_id:
			parent_qs=Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count()==1:
				parent_obj=parent_qs.first()

		
		
		new_comment,created=Comment.objects.get_or_create(
					user=request.user,
					content_type=content_type,
					object_id=obj_id,
					content=content_data,	
					parent=parent_obj,
				)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
		print(created)
	comments=Comment.objects.filter_by_instance(instance)
	# comments=instance.comments

	context={
		"title":"details",
		"instance":instance,
		"share_string":share_string,
		"comments":comments,
		"commentForm":commentForm,
	}
	return render(request,"post_detail.html",context)

def post_list(request):
	queryset_list=Post.objects.active().order_by("-timestamp")
	if request.user.is_staff or request.user.is_superuser:
		queryset_list=Post.objects.all().order_by("-timestamp")
	
	query=request.GET.get("q")
	if query:
		queryset_list=queryset_list.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query)
			).distinct()

	paginator=Paginator(queryset_list, 3)

	page=request.GET.get('page')
	try:
		queryset=paginator.page(page)
	except PageNotAnInteger:
		queryset=paginator.page(1)
	except EmptyPage:
		queryset=paginator.page(paginator.num_pages)

	context={
		"object_list":queryset
	}
	return render(request,"post_list.html",context)

def post_update(request,id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance=get_object_or_404(Post,id=id)
	form=PostForm(request.POST or None,request.FILES or None,instance=instance)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		messages.success(request,"Saved")
		return HttpResponseRedirect(instance.get_absolute_url())
	context={
		"title":"details",
		"instance":instance,
		"form":form
	}
	return render(request,"post_form.html",context)	

def post_delete(request,id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance=get_object_or_404(Post,id=id)
	instance.delete()
	messages.success(request,"uccessfuky deleted")
	return redirect("posts:list")