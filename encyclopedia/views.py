from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

from . import util


def index(request):
    if request.method == 'POST':
        e = request.POST
        print(e['q'])
        entry=util.get_entry(e['q'])
        if entry != None: 
           return render(request, "encyclopedia/getentry.html", {
              "entry": entry,
              "entryname": e['q']
           })
        else:
            return render(request, "encyclopedia/search.html", {
              "l": util.search_entries(e['q']),
              "entryname": e['q'] 
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def getentry(request, entryname):
    return render(request, "encyclopedia/getentry.html", {
        "entry": util.get_entry(entryname),
        "entryname": entryname
    })

def new(request):
    mensaje=''
    if request.method == 'POST':
        e = request.POST
        print(e['title'])
        entry=util.get_entry(e['title'])
        texto=e['texto']
        title=e['title']
        if entry != None: 
           mensaje='Wiki entry allready exists'
           alerttype='alert-warning'   
        else:
        #    mensaje='Wiki entry succesfully added' 
        #    alerttype='alert-success'   
           util.save_entry(title,texto)
           return redirect('getentry', entryname=title)

        return render(request, "encyclopedia/new.html", { 
              "mensaje":mensaje,
              "alerttype":alerttype,
              "texto":texto,
              "title":title


           })
    else:    
        return render(request, "encyclopedia/new.html", {
        
        
    })

def edit(request, entryname):
    mensaje=''
    alerttype=''
    if request.method == 'POST':
        e = request.POST
        texto=e['texto']
        title=e['title']
        mensaje='Wiki entry succesfully updated' 
        alerttype='alert-success'   
        util.save_entry(title,texto)
        return redirect('wiki', entryname=title)
        
    else: 
        return render(request, "encyclopedia/edit.html", {
        "mensaje":mensaje,
        "alerttype":alerttype,
        "texto": util.get_entry2(entryname),
        "title": entryname
    })   
        
def random(request):
    n=util.get_random()
    
    return render(request, "encyclopedia/getentry.html", {
        "entry": util.get_entry(n),
        "entryname": n
    })