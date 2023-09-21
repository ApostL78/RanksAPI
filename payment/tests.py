from unittest.mock import patch

import pytest
from django.urls import reverse

from payment.models import Item, Order
from payment.utils import get_item_session, get_order_session


@pytest.mark.django_db
@pytest.fixture
def new_item():
    item = Item.objects.create(name="Test Item", price=10)
    return item


@pytest.mark.django_db
@pytest.fixture
def new_order():
    item1 = Item.objects.create(name="Test Item 1", price=10)
    item2 = Item.objects.create(name="Test Item 2", price=24)
    order = Order.objects.create()
    order.items.add(item1)
    order.items.add(item2)
    return order


@pytest.mark.django_db
@pytest.mark.parametrize(
    "viewname",
    ["buy", "buy_order"],
)
def test_buy_item_view_success(client, new_item, new_order, viewname):
    obj = None
    if viewname == "buy":
        obj = new_item
    elif viewname == 'buy_order':
        obj = new_order
    url = reverse(viewname, kwargs={"id": obj.id})
    response = client.get(url)
    assert response.status_code == 200
    assert "session_id" in response.json()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "viewname",
    ["buy", "buy_order"],
)
def test_buy_item_view_item_does_not_exist(client, viewname):
    url = reverse(viewname, kwargs={"id": 999})
    response = client.get(url)
    assert response.status_code == 404
    assert f"{'Item' if viewname == 'buy' else 'Order'} with id=999 does not exists" in response.json()["message"]


@pytest.mark.django_db
def test_get_item_session_error(new_item):
    item = new_item
    with patch("stripe.checkout.Session.create") as mock_create:
        mock_create.side_effect = Exception("Test Exception")
        with pytest.raises(Exception):
            get_item_session(item)


@pytest.mark.django_db
def test_get_item_session_error(new_order):
    order = new_order
    with patch("stripe.checkout.Session.create") as mock_create:
        mock_create.side_effect = Exception("Test Exception")
        with pytest.raises(Exception):
            get_order_session(order)


@pytest.mark.django_db
def test_item_view_success(client, new_item):
    item = new_item
    url = reverse("item", kwargs={"pk": item.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context.get("item") == item
    assert "Test Item" in response.content.decode()
    assert "10.00" in response.content.decode()
    assert "payment/item.html" in response.templates[0].name


@pytest.mark.django_db
@pytest.mark.parametrize(
    "viewname",
    ["item", "order"],
)
def test_item_view_item_does_not_exist(client, viewname):
    url = reverse(viewname, kwargs={"pk": 999})
    response = client.get(url)
    assert response.status_code == 404
