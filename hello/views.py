import concurrent.futures
import os
import random
import shutil
import string
import threading
import urllib.request
import zipfile
from os.path import basename

from PIL import Image
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormView
# Create your views here.
from rembg import remove

from gettingstarted.custom_storage import MediaStorage
from .forms import AddForm
from .models import Greeting

media_storage = MediaStorage()


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "home.html")


def db(request):
    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str


class FileFieldFormView(FormView):
    form_class = AddForm
    template_name = 'home.html'  # Replace with your template.
    success_url = '/'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('images')
        if form.is_valid():
            for f in files:
                print(f)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def getfiles(request, filenames):
    filename = 'zip11.zip'
    # filedir = 'results/zip11.zip'
    folder = 'results/'
    baisc_dir = folder + filename
    filepath = os.path.join(settings.MEDIA_ROOT, folder)
    with zipfile.ZipFile(baisc_dir, 'w') as img_zip:
        for image_name in filenames:
            image_url = filenames[image_name]
            url = urllib.request.urlopen(image_url)
            # image = Image.open(requests.get(image_url, stream=True).raw)
            # img_name = os.path.basename(image_path)
            print("url is : " + url)
            img_zip.write(url.read(), image_name)

    img_zip.close()

    file = open(baisc_dir, 'rb')
    fs = FileSystemStorage(location=filepath)  # defaults to   MEDIA_ROOT
    file_name = "myimages" + str(get_random_string(8)) + ".zip"
    file_path_within_bucket = os.path.join("output", file_name)
    # final_file = fs.save(filename, file)
    # file_url = fs.url(final_file)
    media_storage.save(file_path_within_bucket, img_zip)
    file_url = media_storage.url(file_path_within_bucket)
    print("zip file url is : " + str(file_url))
    file.close()
    # final_path = "/results" + str(file_url)
    request.session['final_file'] = file_url
    # return file_url


def append_output(image):
    fname = os.path.splitext(image.name)[0]
    image_name = str(fname) + ".PNG"
    output_path = os.path.join(settings.BASE_DIR, 'images', image_name)
    return output_path


def delete_old_files(folder):
    # folder = loc
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def process_image(image):
    fname = os.path.splitext(image.name)[0]
    image_name = str(fname) + ".PNG"
    output_path = os.path.join(settings.BASE_DIR, 'images', image_name)
    # print("output_path is : "+ str(output_path))
    input = Image.open(image)
    output = remove(input)
    # format = 'png'
    image_path_within_bucket = os.path.join("images", image_name)
    print("image_path_within_bucket is : " + image_path_within_bucket)
    output.save(output_path)
    image = open(output_path, 'rb')
    # media_storage.save(image_path_within_bucket, image)
    # image_url = media_storage.url(image_path_within_bucket)
    # print("image url is : " + str(image_url))
    # # bg_removed_images.append(str(output_path))
    # print(image_url)


def form_handle(request):
    form = AddForm()
    if request.method == 'POST':
        form = AddForm(request.POST, request.FILES or None)
        if form.is_valid():
            cd = form.cleaned_data
            # now in the object cd, you have the form as a dictionary.
            files = request.FILES.getlist('images')
            # x = 1
            # y = 1
            # images_list = {}
            bg_removed_images = []
            for image in files:
                print()
                bg_removed_images.append(str(append_output(image)))
            executor = concurrent.futures.ProcessPoolExecutor(10)
            futures = [executor.submit(process_image, item) for item in files]
            concurrent.futures.wait(futures)
            print('converting was done')
            baisc_dir = 'images5.zip'
            with zipfile.ZipFile(baisc_dir, 'w') as img_zip:
                for image_path in bg_removed_images:
                    print(image_path)
                    img_zip.write(image_path, basename(image_path))
                img_zip.close()
            print('zipping was done')
            file = open(baisc_dir, 'rb')
            file_name = "myimages" + get_random_string(8) + ".zip"
            file_path_within_bucket = os.path.join("output", file_name)
            # media_storage.save(file_path_within_bucket, file)
            # file_url = media_storage.url(file_path_within_bucket)
            print('uploading was done')
            # print("zip file url is : " + str(file_url))
            # request.session['final_file'] = str(file_url)
            output_path = os.path.join(settings.BASE_DIR, 'images')
            delete_old_files(output_path)
            form = AddForm()
            # return HttpResponseRedirect(str(file_url))
            return HttpResponseRedirect(reverse('home'))
    return render(request, "index.html", {"form": form})


def form_handle2(request):
    form = AddForm()
    if request.method == 'POST':
        form = AddForm(request.POST, request.FILES or None)
        if form.is_valid():
            cd = form.cleaned_data
            # now in the object cd, you have the form as a dictionary.
            files = request.FILES.getlist('images')
            x = 1
            y = 1
            images_list = {}
            bg_removed_images = []
            print("first images are: ")
            x = 1
            for image in files:
                images_list[x] = image
                x = x + 1
            print(images_list)
            print(x)
            for y in range(y, x, 3):
                y2 = int(y) + 1
                y3 = int(y) + 2
                if y3 < x:
                    t1 = threading.Thread(target=process_image, args=(images_list[y],))
                    t2 = threading.Thread(target=process_image, args=(images_list[y2],))
                    t3 = threading.Thread(target=process_image, args=(images_list[y3],))
                    t1.start(), t2.start(), t3.start()
                    t1.join(), t2.join(), t3.join()
                    bg_removed_images.append(str(append_output(images_list[y])))
                    bg_removed_images.append(str(append_output(images_list[y2])))
                    bg_removed_images.append(str(append_output(images_list[y3])))
                elif y2 < x:
                    t1 = threading.Thread(target=process_image, args=(images_list[y],))
                    t2 = threading.Thread(target=process_image, args=(images_list[y2],))
                    t1.start(), t2.start()
                    t1.join(), t2.join()
                    bg_removed_images.append(str(append_output(images_list[y])))
                    bg_removed_images.append(str(append_output(images_list[y2])))
                else:
                    t1 = threading.Thread(target=process_image, args=(images_list[y],))
                    t1.start()
                    t1.join()
                    bg_removed_images.append(str(append_output(images_list[y])))

            print('bg_removed_images is ::')
            print(bg_removed_images)
            baisc_dir = 'images4.zip'
            with zipfile.ZipFile(baisc_dir, 'w') as img_zip:
                for image_path in bg_removed_images:
                    img_zip.write(image_path)
                img_zip.close()
            file = open(baisc_dir, 'rb')
            file_name = "myimages" + get_random_string(8) + ".zip"
            file_path_within_bucket = os.path.join("output", file_name)
            media_storage.save(file_path_within_bucket, file)
            file_url = media_storage.url(file_path_within_bucket)
            print("zip file url is : " + str(file_url))
            request.session['final_file'] = str(file_url)
            form = AddForm()
            # return HttpResponseRedirect(str(file_url))
            return HttpResponseRedirect(reverse('home'))
    return render(request, "index.html", {"form": form})


def downlaod_images(request, file):
    file_link = file
    try:
        file_name = request.session['final_file']
    except:
        file_name = None
    if file_name is None:
        print("file_name is None")
        return HttpResponseRedirect(reverse('home'))
    else:
        if file_link != file_name:
            print("file_name is not equal with session name")
            return HttpResponseRedirect(reverse('home'))
        else:
            filepath = os.path.join(settings.MEDIA_ROOT, "results")
            fs = FileSystemStorage(location=filepath)
            out_file = fs.path(file_link)
            the_file3 = open(out_file, 'rb')
            the_file = "/media/results" + str(out_file)
            print(" the file is : " + str(the_file))
            response = FileResponse(the_file3)

            # serv = serve(request, str(the_file))
            return response
