from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from rembg import remove
from PIL import Image
import os
from .forms import AddForm
from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})


def form_handle(request):
    form = AddForm()
    if request.method == 'POST':
        form = AddForm(request.POST, request.FILES or None)
        if form.is_valid():
            cd = form.cleaned_data
            # now in the object cd, you have the form as a dictionary.
            files = request.FILES.getlist('images')
            # print(a)
            x = 1
            # temp = tempfile.TemporaryFile()
            # archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
            for image in files:
                fname = os.path.splitext(image.name)[0]
                print("fname is : "+ str(fname))
                output_path ="images/"+ str(fname) + ".png"
                input = Image.open(image)
                output = remove(input)
                output.save(output_path)
            #     archive.write(output_path)
            # archive.close()

            # temp.seek(1)
            # wrapper = FileWrapper(temp)
            # response = HttpResponse(wrapper, content_type='application/zip')
            # response['Content-Disposition'] = 'attachment; filename=test2.zip'

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return render(request, "home.html", {"form": form})