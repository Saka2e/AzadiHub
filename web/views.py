from django.shortcuts import render
from django.core.paginator import Paginator
from crawler.models import Config

def index(request):
    config_count = Config.objects.count()  # محاسبه تعداد کانفیگ‌ها از دیتابیس
    return render(request, 'index.html', {'config_count': config_count})

def configs(request):
    protocol = request.GET.get('protocol', '')
    if protocol:
        configs = Config.objects.filter(protocol=protocol)
    else:
        configs = Config.objects.all()
    
    # صفحه‌بندی: 20 کانفیگ در هر صفحه
    paginator = Paginator(configs, 21)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'configs.html', {
        'configs': page_obj,
        'protocol': protocol
    })

def donation(request):
    return render(request, 'donation.html')

def faq(request):
    return render(request, 'faq.html')