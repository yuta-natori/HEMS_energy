from django.urls import path
from .views import index_views
from .views import trend_analysis_views

app_name = 'app'
urlpatterns = [
  path('', index_views.index,  name='index'),
  path('holiday', index_views.holiday,  name='holiday'),
  path('temperature', index_views.temperature,  name='temperature'),
  path('electric_power', index_views.electric_power,  name='electric_power'),
  path('toukei_keisan', index_views.toukei_keisan,  name='toukei_keisan'),
  path('jyuyou_class', index_views.jyuyou_class, name='jyuyou_class'),
  path('jyuyou_trend', trend_analysis_views.jyuyou_trend, name='jyuyou_trend'),
  path('execute_trend', trend_analysis_views.execute_trend, name='execute_trend'),
  path('jyuyou_modeling', index_views.jyuyou_modeling, name='jyuyou_modeling'),
  path('chouki_yosoku', index_views.chouki_yosoku, name='chouki_yosoku'),
  path('tanki_yosoku', index_views.tanki_yosoku, name='tanki_yosoku'),
]