
from django.shortcuts import render, redirect, get_object_or_404
from properties.models import Property
from django.db.models import Q


def home(request):
    featured_properties = Property.objects.filter(status='AVAILABLE').order_by('-created_at')[:6]
    sold_properties = Property.objects.filter(status='SOLD').order_by('-created_at')
    return render(request, 'website/home.html', {
        'featured_properties': featured_properties,
        'sold_properties': sold_properties,
    })


def property_search(request):
    if request.user.is_authenticated and getattr(request.user, 'role', '') == 'PROPERTY':
        return redirect('property_list')

    properties = Property.objects.filter(
        status='AVAILABLE'
    ).order_by('-created_at')
    listing_type = request.GET.get('listing_type')
    if listing_type in ('SALE', 'RENT'):
        properties = properties.filter(listing_type=listing_type)

    # Property type
    property_type = request.GET.get('type')

    if property_type:
        properties = properties.filter(
            property_type=property_type
        )

    # City
    city = request.GET.get('city')

    if city:
        properties = properties.filter(Q(city__icontains=city) | Q(location__icontains=city))

    # District
    district = request.GET.get('district')

    if district:
        properties = properties.filter(Q(district__icontains=district) | Q(location__icontains=district))

    # Minimum and maximum bedrooms
    min_bedrooms = request.GET.get('min_bedrooms')
    max_bedrooms = request.GET.get('max_bedrooms')

    if min_bedrooms:
        properties = properties.filter(
            bedrooms__gte=min_bedrooms
        )

    if max_bedrooms:
        properties = properties.filter(
            bedrooms__lte=max_bedrooms
        )

    # Bathrooms
    bathrooms = request.GET.get('bathrooms')

    if bathrooms:
        properties = properties.filter(
            bathrooms__gte=bathrooms
        )

    # House IDs are generated as LGS-000001 from the property's database ID.
    property_id = request.GET.get('property_id', '').strip().upper()
    if property_id:
        if property_id.startswith('LGS-'):
            property_id = property_id[4:]
        if property_id.isdigit():
            properties = properties.filter(pk=int(property_id))
        else:
            properties = properties.none()

    # Minimum and maximum price
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    price_field = 'monthly_rent' if listing_type == 'RENT' else 'price'
    if min_price:
        properties = properties.filter(**{f'{price_field}__gte': min_price})

    if max_price:
        properties = properties.filter(**{f'{price_field}__lte': max_price})

    # Minimum and maximum floor area
    min_area = request.GET.get('min_area')
    max_area = request.GET.get('max_area')

    if min_area:
        properties = properties.filter(
            area__gte=min_area
        )

    if max_area:
        properties = properties.filter(
            area__lte=max_area
        )

    # Keyword search
    keyword = request.GET.get('keyword')

    if keyword:
        properties = properties.filter(
            Q(title__icontains=keyword) |
            Q(location__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(features__icontains=keyword)
        )

    # Other features
    if request.GET.get('swimming_pool'):
        properties = properties.filter(
            swimming_pool=True
        )

    if request.GET.get('parking'):
        properties = properties.filter(
            parking=True
        )

    if request.GET.get('garden'):
        properties = properties.filter(
            garden=True
        )

    if request.GET.get('furnished'):
        properties = properties.filter(
            furnished=True
        )

    return render(request, 'website/property_search.html', {
        'properties': properties,
    })


def property_detail(request, pk):
    property_obj = get_object_or_404(
        Property.objects.prefetch_related('photos'),
        pk=pk,
        status__in=['AVAILABLE', 'SOLD'],
    )
    gallery_photos = []
    if property_obj.image:
        gallery_photos.append({'url': property_obj.image.url, 'caption': property_obj.title})
    gallery_photos.extend(
        {'url': photo.image.url, 'caption': photo.caption or property_obj.title}
        for photo in property_obj.photos.all()
    )
    return render(request, 'website/property_detail.html', {
        'property': property_obj,
        'gallery_photos': gallery_photos,
        'similar_properties': Property.objects.filter(
            status='AVAILABLE',
            listing_type=property_obj.listing_type,
            property_type=property_obj.property_type,
        ).exclude(pk=property_obj.pk).order_by('-created_at')[:3],
    })
