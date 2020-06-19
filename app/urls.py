from django.urls import path
from .views import index_views
from .views import trend_analysis_views
from .views import demand_class_views
from .views import demand_modeling_views
from .views import short_term_forecast_views

app_name = 'app'
urlpatterns = [
  path('', index_views.index,  name='index'),
  path('holiday', index_views.holiday,  name='holiday'),
  path('temperature', index_views.temperature,  name='temperature'),
  path('electric_power', index_views.electric_power,  name='electric_power'),
  path('toukei_keisan', index_views.toukei_keisan,  name='toukei_keisan'),
  path('jyuyou_trend', trend_analysis_views.jyuyou_trend, name='jyuyou_trend'),
  path('execute_trend', trend_analysis_views.execute_trend, name='execute_trend'),
  #需要クラス別分析
  path('jyuyou_class', index_views.demand_class, name='jyuyou_class'),
  path('analysis_demand_class', demand_class_views.analysis_demand_class, name='analysis_demand_class'),
  #需要モデリング
  path('jyuyou_modeling', index_views.jyuyou_modeling, name='jyuyou_modeling'),
  path('demand_modeling', demand_modeling_views.demand_modeling, name='demand_modeling'),
  
  path('chouki_yosoku', index_views.chouki_yosoku, name='chouki_yosoku'),
  #短期需要予測
  path('tanki_yosoku', index_views.tanki_yosoku, name='tanki_yosoku'),
  path('short_term_forecast', short_term_forecast_views.short_term_forecast, name='short_term_forecast'),
]