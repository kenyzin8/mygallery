from django.shortcuts import render
from .models import *
from django.http import JsonResponse

def home(request):
    categories = Category.objects.filter(is_active=True)
    selected_category = request.GET.get('category', 'all')

    if selected_category == 'all':
        images = Image.objects.filter(is_active=True)
    else:
        images = Image.objects.filter(is_active=True, category__name=selected_category)

    image_ids = [image.id for image in images]

    help_icon_content = HelpIconContent.objects.first()

    context = {
        'categories': categories,
        'images': images,
        'selected_category': selected_category,
        'image_ids': image_ids,
        'help_icon_content': help_icon_content,
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