from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

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

    columns = {i: [] for i in range(grid_columns)}
    for index, image in enumerate(images_page):
        columns[index % grid_columns].append(image)

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

def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def has_viewed(image_id, session_id, ip_address):
    return ImageView.objects.filter(image_id=image_id, session_id=session_id, ip_address=ip_address).exists()

def record_view(image_id, session_id, ip_address):
    new_view = ImageView(image_id=image_id, session_id=session_id, ip_address=ip_address)
    new_view.save()

def get_image_preview(request):
    try:
        image_id = request.GET.get('image_id', None)
        user_session_id = request.session.session_key
        user_ip_address = get_user_ip(request) 

        image = Image.objects.get(id=image_id)

        if not has_viewed(image_id, user_session_id, user_ip_address):
            record_view(image_id, user_session_id, user_ip_address)

        return JsonResponse({
            'success': True,
            'image_url': image.image.url,
            'image_title': f'{image.title} · {image.image_width}x{image.image_height} · {image.description}' if image.description else f'{image.title} · {image.image_width}x{image.image_height}',
            'total_views': f'{ImageView.objects.filter(image_id=image_id).count()} views' if ImageView.objects.filter(image_id=image_id).count() > 1 else f'{ImageView.objects.filter(image_id=image_id).count()} view',
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
