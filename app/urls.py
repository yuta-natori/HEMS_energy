from django.urls import path
from .views import index_views
from .views import demand_class_views
from .views import demand_modeling_views

app_name = 'app'
urlpatterns = [
  path('', index_views.index,  name='index'),
  path('holiday', index_views.holiday,  name='holiday'),
  path('temperature', index_views.temperature,  name='temperature'),
  path('electric_power', index_views.electric_power,  name='electric_power'),
  path('toukei_keisan', index_views.toukei_keisan,  name='toukei_keisan'),
  #需要クラス別分析
  path('jyuyou_class', index_views.demand_class, name='jyuyou_class'),
  path('analysis_demand_class', demand_class_views.analysis_demand_class, name='analysis_demand_class'),
  
  path('jyuyou_trend', index_views.jyuyou_trend, name='jyuyou_trend'),
  #需要モデリング
  path('jyuyou_modeling', index_views.jyuyou_modeling, name='jyuyou_modeling'),
  path('demand_modeling', demand_modeling_views.demand_modeling, name='demand_modeling'),
  
  path('chouki_yosoku', index_views.chouki_yosoku, name='chouki_yosoku'),
  path('tanki_yosoku', index_views.tanki_yosoku, name='tanki_yosoku'),
]