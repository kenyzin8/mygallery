from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import islice

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

    grid_columns = GridColumns.objects.first().number_of_columns

    is_mobile = request.device['is_mobile']
    
    if is_mobile:
        grid_columns = 2

    latest_images = list(islice(images_page, grid_columns))
    columns = {i: [latest_images[i]] if i < len(latest_images) else [] for i in range(grid_columns)}

    target_height = sum(img.image_height or 0 for img in columns[0])

    remaining_images = sorted(images_page[grid_columns:], key=lambda x: x.image_height or 0, reverse=True)

    for image in remaining_images:
        suitable_column = min(columns, key=lambda x: (target_height - sum(img.image_height or 0 for img in columns[x])) if target_height >= sum(img.image_height or 0 for img in columns[x]) else float('inf'))
        
        columns[suitable_column].append(image)

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
        'grid_columns': grid_columns,
        'is_mobile': is_mobile,
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