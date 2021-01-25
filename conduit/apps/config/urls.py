from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ConfigViewset

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'config', ConfigViewset, basename='user')
urlpatterns = router.urls

#urlpatterns = {
#    url(r'^config/$', ConfigViewset.as_view({'get': 'list','post': 'create'}), name="create"),
#}

#urlpatterns = format_suffix_patterns(urlpatterns)



# urlpatterns = [
# 	path('config/', views.configList,name="config_list"),
# 	path('config?name=<str:pk>', views.configDetail,name="config_detil"),
# ]




