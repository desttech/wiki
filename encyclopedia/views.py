from secrets import choice
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
import markdown2 # Text to HTML convertor, see https://github.com/trentm/python-markdown2
from . import util #CS50W helper functions
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page(request, entry):
    """ Renders markdown file in HTML page """

    # convert the markdown file to string 
    content = util.get_entry(entry)

    if content == None:
        return render(request,"encyclopedia/result.html", {
            "message" : "Error 404 page was not found"
        })

    markdown_text = markdown2.markdown(content)

    # Renders the page
    return render(request,"encyclopedia/page.html", {
        'entry' : entry,
        'content' : markdown_text
    })

def search(request, ):
    "search the markdown files"
    if request.method == "POST":
        # Get the search term from the input
        term = request.POST
        term = term['q']
    

        entries = util.list_entries()
        page = None

        for item in entries:
            if item.lower() == term.lower():
                page = item
                print("Exact match found!", page)

        # Redirect to page of Exact match
        if page != None:
            return HttpResponseRedirect(reverse("encyclopedia:page", kwargs={'entry': page}))

         # checks if the query is a substring of the name of any entry in the encyclopedia   
        found=[]
        for item in entries :
            if term.lower() in item.lower():
                found.append(item)

        # if there is not match
        if not found:
            return render(request,"encyclopedia/results.html",)

        # if there is or are matches 
        else:
            return render(request,"encyclopedia/results.html",{
                'results' : found
            })

def new(request):
    """Creates a new markdown file via an HTML form"""
    # if the site is visited through the create new page link
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")   
    # if the form is sumbitted
    if request.method == "POST":
        form_data = request.POST
        title = form_data['title']
        content = form_data['content']

        entries = util.list_entries()
        for item in entries:
            # check if title name already exists 
            if item.lower() == title.lower():
                return render(request, "result.html", {
                    'message' : "Error! New entry was not added because title already exists, change the name and try again"
                })

            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:index"))

def edit(request,entry):
    """ Edit markdown file """
    if request.method == "GET":
        content = util.get_entry(entry)

        return render(request,"encyclopedia/edit.html", {
            "title" : entry ,
            "content" : content

        })
    if request.method == "POST":
        form = request.POST
        title = form['title']
        content = form['content']

        util.save_entry(title,content)

        return HttpResponseRedirect(reverse("encyclopedia:page", kwargs={'entry': title}))
def random_page(request):
    entries = util.list_entries()
    page= random.choice(entries)
    return HttpResponseRedirect(reverse("encyclopedia:page", kwargs={'entry': page}))


