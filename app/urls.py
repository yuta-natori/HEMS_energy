from django.urls import path
from .views import index

app_name = 'app'
urlpatterns = [
  path('', index.index,  name='index'),
  path('holiday', index.holiday,  name='holiday'),
  path('temperature', index.temperature,  name='temperature'),
  path('electric_power', index.electric_power,  name='electric_power'),
  path('toukei_keisan', index.toukei_keisan,  name='toukei_keisan'),
  path('jyuyou_class', index.jyuyou_class, name='jyuyou_class'),
  path('jyuyou_trend', index.jyuyou_trend, name='jyuyou_trend'),
  path('jyuyou_modeling', index.jyuyou_modeling, name='jyuyou_modeling'),
  path('chouki_yosoku', index.chouki_yosoku, name='chouki_yosoku'),
  path('tanki_yosoku', index.tanki_yosoku, name='tanki_yosoku'),
]