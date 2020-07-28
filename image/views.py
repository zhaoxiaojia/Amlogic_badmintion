from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.utils.decorators import method_decorator

from .forms import ImageForm
from .models import Image


# Create your views here.

@login_required()
@csrf_exempt
@require_POST
def upload_image(request):
    title = request.POST.get('title')
    description = request.POST.get('description')
    photo = request.FILES.get('photo')
    try:
        if Image.objects.filter(title=title):
            return HttpResponseRedirect('/image/list_image')
        Image.objects.create(user=request.user, image=photo, title=title, description=description)
        return HttpResponseRedirect('/image/list_image')
    except:
        return HttpResponse('数据错误')
    # form = ImageForm(data=request.POST)
    #
    # if form.is_valid():
    #     print('valid')
    #     try:
    #         new_item = form.save(commit=False)
    #         new_item.user = request.user
    #         new_item.save()
    #         return JsonResponse({'status': '1'})
    #     except:
    #         return JsonResponse({'status': '0'})


@method_decorator(login_required,'dispatch')
class ImageList(ListView):
    model = Image
    template_name = 'image/list_images.html'
    context_object_name = 'images'
    paginate_by = 5

@login_required(login_url='/account/lobin/')
@require_POST
@csrf_exempt
def del_image(request):
    image_id = request.POST['image_id']
    try:
        image = Image.objects.filter(id=image_id)
        image.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('数据错误')

def falls_images(request):
    images = Image.objects.all()
    return render(request, 'image/falls_images.html', {"images": images})