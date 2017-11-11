from django.shortcuts import render,get_object_or_404
from .models import Comment
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

# Create your views here.
@login_required(login_url='/login/')
def comment_delete(request,id=None):
	# obj=Comment.objects.get(id=id)
	try:
		obj=Comment.objects.get(id=id)
	except:
		raise Http404
	if obj.user != request.user:
		response=HttpResponse("You don't have permission to see this")
		response.status_code=403
		return response
	if request.method=="POST":
		parent_obj_url=obj.content_object.get_absolute_url()
		obj.delete()
		return HttpResponseRedirect(parent_obj_url)
	context={
		"object":obj,
	}
	return render(request,"confirm_delete.html",context) 

# @login_required(login_url='/login/')
def comment_thread(request,id):
	# obj=Comment.objects.get(id=id)
	try:
		obj=Comment.objects.get(id=id)
	except:
		raise Http404

	if not obj.is_parent:
		obj=obj.parent

	content_object=obj.content_object
	content_id=obj.content_object.id

	initial_data={
		"content_type":obj.content_type,
		"object_id":obj.object_id
	}

	commentForm=CommentForm(request.POST or None,initial=initial_data)
	if commentForm.is_valid():
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

		
		print(parent_obj)
		new_comment,created=Comment.objects.get_or_create(
					user=request.user,
					content_type=content_type,
					object_id=obj_id,
					content=content_data,	
					parent=parent_obj,
				)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
	context={
	"comment":obj,
	"form":commentForm,
	}
	return render(request,"comment_thread.html",context)