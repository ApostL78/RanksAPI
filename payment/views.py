from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView

from payment.models import Item, Order
from payment.utils import get_item_session, get_order_session


class BuyItemView(View):

    def get(self, request, id):
        # Получаем информацию о товаре с заданным id
        try:
            item = Item.objects.get(id=id)
        except Item.DoesNotExist:
            return JsonResponse(status=404, data={
                "message": f"Item with id={id} does not exists"})

        # Создаем Stripe Session
        try:
            session = get_item_session(item)
        except Exception as e:
            return JsonResponse(status=400, data={"message": str(e)})

        # Возвращаем Session ID в формате JSON
        return JsonResponse({"session_id": session.id})


class BuyOrderView(View):

    def get(self, request, id):
        # Получаем информацию о заказе с заданным id
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            return JsonResponse(status=404, data={
                "message": f"Order with id={id} does not exists"})

        # Создаем Stripe Session
        try:
            session = get_order_session(order)
        except Exception as e:
            return JsonResponse(status=400, data={"message": str(e)})

        # Возвращаем Session ID в формате JSON
        return JsonResponse({"session_id": session.id})


class ItemView(DetailView):
    model = Item
    template_name = "payment/item.html"
    context_object_name = "item"


class OrderView(DetailView):
    model = Order
    template_name = "payment/order.html"
    context_object_name = "order"
