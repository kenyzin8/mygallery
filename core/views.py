from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    categories = Category.objects.filter(is_active=True)
    selected_category = request.GET.get('category', 'all')

    if selected_category == 'all':
        images = Image.objects.filter(is_active=True).order_by('-id')
    else:
        images = Image.objects.filter(is_active=True, category__name=selected_category).order_by('-id')

    page = request.GET.get('page', 1)
    paginator = Paginator(images, 36)

    try:
        images_page = paginator.page(page)
    except PageNotAnInteger:
        images_page = paginator.page(1)
    except EmptyPage:
        images_page = paginator.page(paginator.num_pages)

    columns = {i: [] for i in range(4)}
    for index, image in enumerate(images_page):
        columns[index % 4].append(image)

    help_icon_content = HelpIconContent.objects.first()

    image_ids = [image.id for image in images_page]

    context = {
        'categories': categories,
        'columns': columns.values(),
        'selected_category': selected_category,
        'help_icon_content': help_icon_content,
        'paginator': paginator, 
        'page_obj': images_page,  
        'image_ids': image_ids,
    }

    return render(request, 'home.html', context)


def get_image_preview(request):
    try:
        image_id = request.GET.get('image_id', None)
        image = Image.objects.get(id=image_id)

        return JsonResponse({
            'success': True,
            'image_url': image.image.url,
            'image_title': f'{image.title} · {image.image_width}x{image.image_height} · {image.description}' if image.description else f'{image.title} · {image.image_width}x{image.image_height}',
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})