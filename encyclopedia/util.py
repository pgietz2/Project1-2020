import re,random

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def mymarkdown(lines): # (c) 2020 by Pablo Gietz
    stack=[]
    def sr(where,search,init,end):
        while where.find(search)>0:
            x=-1
            if search in stack: x=''.join(stack).rindex(search)
            if x>=0:
               stack.pop(x)
               where=where.replace(search,end,1)
            else:  
               stack.append(search)
               where=where.replace(search,init,1)
        return where
    ul=False
    r = []
    for l in lines:
        # search for headings
        p = re.compile(r"\[(.+?)\]\((.+?)\)")
        x=p.findall(l)
             
        if x:
            for d in x:
                xlink='<a href="'+d[1]+'">'+d[0]+'</a>'
                print(xlink)
                l=l.replace(p.search(l).group(0),xlink)

        fw = l.strip().partition(' ')[0]  # first word
        p = l.strip().partition(' ')[2]
        h = l.strip()
        if fw == '#':            h = '<h1>'+p+'</h1>'
        if fw == '##':           h = '<h2>'+p+'</h2>'
        if fw == '###':          h = '<h3>'+p+'</h3>'
        if fw == '####':         h = '<h4>'+p+'</h4>'
        if fw == '#####':        h = '<h5>'+p+'</h5>'
        if fw == '######':       h = '<h6>'+p+'</h6>'
        if fw == '-':  
           if not ul:
              ul=True
              r.append('<ul>') 
           h = '<li>'+p+'</li>' 
        else: 
            if ul:
                r.append('</ul>')
                ul=False
        
        h=sr(h,'***','<b><i>','</i></b>')  
        h=sr(h,'**','<b>','</b>')  

        r.append(h)
    return r




def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"

    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = open(f"entries/{title}.md")
   
        lines = mymarkdown(f.readlines())
     
        return lines

        # f = default_storage.open(f"entries/{title}.md")
        # return f.read().decode("utf-8")
        # f = default_storage.open(f"entries/{title}.md")
        # l=f.readlines()
        # return l
    except FileNotFoundError:
        return None
        
def get_entry2(title):
    try:
        with open(f"entries/{title}.md", 'r') as file: 
            # lines = file.read().replace('\n', chr(13)).replace('\r', chr(10))
            lines = file.read().replace('\n\n', chr(13))        
        # f = open(f"entries/{title}.md")
        # lines = f.readlines()
        return lines
               
    except FileNotFoundError:
        return None

def search_entries(texto):
    """
    Returns a list of all names of encyclopedia entries that contains the text.
    """
    l=[]
    _, filenames = default_storage.listdir("entries")
    for filename in filenames:
        if texto.upper() in re.sub(r"\.md$", "", filename).upper():
           l.append(re.sub(r"\.md$", "", filename))
    return l

def get_random():
    _, filenames = default_storage.listdir("entries")
    l=[]
    for filename in filenames:
        if filename.endswith(".md"):
           l.append(re.sub(r"\.md$", "", filename))
   
    return random.choice(l)
#     return list(sorted(re.sub(r"\.md$", "", filename)
#                 for filename in filenames if filename.endswith(".md")))
# with open('example.txt') as f:
#     if 'blabla' in f.read():
#         print("true")
