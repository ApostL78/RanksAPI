from django.urls import path

from payment.views import BuyItemView, ItemView, OrderView, BuyOrderView

urlpatterns = [
    path("buy/<int:id>", BuyItemView.as_view(), name="buy"),
    path("item/<int:pk>", ItemView.as_view(), name="item"),
    path("order/<int:pk>", OrderView.as_view(), name="order"),
    path("buy_order/<int:id>", BuyOrderView.as_view(), name="buy_order"),
]