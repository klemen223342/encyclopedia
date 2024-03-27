from django.urls import path,include

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("create",views.createEntry,name="create_entry"),
    path("wiki/<str:entry>",views.entries,name="entries"),
    path("random",views.randomFile,name="random")
    
    
]
