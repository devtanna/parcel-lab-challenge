import pytest
from track_and_trace.models import Address, Article, Carrier, Shipment


@pytest.mark.django_db
def test_carrier_model():
    name = "Carrier 1"
    carrier = Carrier.objects.create(name=name)
    assert carrier.name == name
    assert str(carrier) == name


@pytest.mark.django_db
def test_address_model():
    address_text = "123 Main St, City"
    address = Address.objects.create(address=address_text)
    assert address.address == address_text
    assert str(address) == address_text


@pytest.mark.django_db
def test_article_model():
    name = "Article 1"
    quantity = 10
    price = 9.99
    sku = "SKU123"
    article = Article.objects.create(name=name, quantity=quantity, price=price, sku=sku)
    assert article.name == name
    assert article.quantity == quantity
    assert article.price == price
    assert article.sku == sku
    assert str(article) == name


@pytest.mark.django_db
def test_shipment_model():
    tracking_number = "TRACK123"
    carrier = Carrier.objects.create(name="Carrier 1")
    sender_address = Address.objects.create(address="Sender Address")
    receiver_address = Address.objects.create(address="Receiver Address")
    article = Article.objects.create(name="Article 1", quantity=10, price=9.99, sku="SKU123")
    shipment = Shipment.objects.create(
        tracking_number=tracking_number,
        carrier=carrier,
        sender_address=sender_address,
        receiver_address=receiver_address,
        article=article,
    )
    assert shipment.tracking_number == tracking_number
    assert shipment.carrier == carrier
    assert shipment.sender_address == sender_address
    assert shipment.receiver_address == receiver_address
    assert shipment.article == article
    assert str(shipment) == tracking_number
