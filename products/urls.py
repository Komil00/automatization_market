from django.urls import path, include
from django.db import router
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from rest_framework_swagger.views import get_swagger_view
from django.conf import settings
from django.conf.urls import static
from users.views import *
from savdo.views import *
from products.views import *
from moliya.views import *



router = SimpleRouter()
router.register('mijoz', MijozViewSet)
router.register('mahsulot', MahsulotlarViewSet)
router.register('mahsulot_olchov', MahsulotOlchovViewSet)
router.register('tolovlar', TolovViewSet)
router.register('moliya_chiqim', MoliyaChiqimViewSet)
router.register('ombor', OmborViewSet)
router.register('ishchi', IshchiViewSet)
router.register('analitika', AnalitikaViewSet)
router.register('tranzaksiya', TranzaksiyaViewSet)
router.register("tolovlar", TolovViewSet)
router.register("savdolar", SavdoViewSet)

router.register("savdosta", SavdoStaViewSet)


router.register("savdolar_pro", SavdoProductViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("savdo/", SavdoCreateView.as_view()),
    # path("savdo_pro/", SavdoProductCreateView.as_view()),
    
    path("tolov/<int:pk>", MijozTolovlarView.as_view(), name="tolov"),
    path("savdo/<int:pk>", SavdoAPIView.as_view()),
    path("mijoz/<int:pk>", MijozOrderHistoryView.as_view(), name="order-history"),

    path('savdo_pro/', SavdoProductListCreateAPIView.as_view(), name='bulk-create')

]
