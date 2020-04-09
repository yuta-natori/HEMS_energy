from django.urls import path
from . import views

app_name = 'app'
urlpatterns = [
  path('', views.index,  name='index'),
  path('holiday', views.holiday,  name='holiday'),
  path('temperature', views.temperature,  name='temperature'),
  path('toukei_keisan', views.toukei_keisan,  name='toukei_keisan'),
  path('jyuyou_class', views.jyuyou_class, name='jyuyou_class'),
  path('jyuyou_trend', views.jyuyou_trend, name='jyuyou_trend'),
  path('jyuyou_modeling', views.jyuyou_modeling, name='jyuyou_modeling'),
  path('chouki_yosoku', views.chouki_yosoku, name='chouki_yosoku'),
  path('tanki_yosoku', views.tanki_yosoku, name='tanki_yosoku'),
]