from django.contrib import admin

# Register your models here.
from .models import Post

class PostAdmin(admin.ModelAdmin):
	"""docstring for PostAdmin"""
	list_display=["__str__","timestamp"]
	class Meta:
		model=Post

admin.site.register(Post,PostAdmin)
