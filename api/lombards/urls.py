from django.conf.urls import url
from .views import percent, filials, goldPrices
urlpatterns = [
    url(r'percent/$', percent, name='percent'),
    url(r'filials/$', filials, name='filial'),
    url(r'prices/$', goldPrices, name='prices')
]
