from django.shortcuts import render
from django.shortcuts import HttpResponse
from django import forms
import markdown2

from django.urls import reverse
from django.http import HttpResponseRedirect


from . import util
import random

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off','class':'search','placeholder':'Search'}))

class PageTitle(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off','id':'title', 'class':'form-control w-25','placeholder':'Select title'}))

class TextForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off','id':'text','class':'form-control w-25 my-5 h-50','placeholder':'Your text'}))

def index(request):

    if request.method == "POST":

        form = SearchForm(request.POST)

        if form.is_valid():

            entry = form.cleaned_data['search']



            if util.get_entry(entry) == None:

                entries =  util.list_entries()

                entries = [s for s in entries if entry in s]

                return render(request,"encyclopedia/possible.html",{

                   "entries":entries

                })
            else:

                return HttpResponseRedirect(reverse("encyclopedia:entries", args=[entry]))


    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":SearchForm()
       
        
    })

def entries(request,entry):

    markdown_file_path = f"entries/{entry}.md"

   

    try:
        with open(markdown_file_path,'r') as f:
            content = f.read()

    except :
        return render(request,"encyclopedia/error.html")
        

    html = markdown2.markdown(content)

    return render(request,"encyclopedia/entry.html",{
        'entry':entry,
        'html':html

    })



def createEntry(request):

    if request.method == "POST":
        title_form = PageTitle(request.POST)
        text_form = TextForm(request.POST)

        if title_form.is_valid() and text_form.is_valid():

            title = title_form.cleaned_data['title']
            text = text_form.cleaned_data['text'] 
            util.save_entry(title,text)
            return HttpResponseRedirect(reverse('encyclopedia:index'))
        else:
            return render(request,"encyclopedia/error.html")

    return render(request,"encyclopedia/createEntry.html",{
        "title":PageTitle(),
        "text":TextForm()


    })

def randomFile(request):

    file_array = util.list_entries()

    random_num = random.randint(0,len(file_array)-1)

    markdown_file_path = f"entries/{file_array[random_num]}.md"

    with open(markdown_file_path,'r') as f:
        file = f.read()

    file = markdown2.markdown(file)
    return render(request,"encyclopedia/random.html",{

        'html':file


    })


    
    







