import csv

from django.core.management.base import BaseCommand

from track_and_trace.models import Address, Article, Carrier, Shipment


class Command(BaseCommand):
    help = 'Insert seed data for shipments'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file containing shipment data')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tracking_number = row['tracking_number']
                carrier = row['carrier']
                sender_address = row['sender_address']
                receiver_address = row['receiver_address']
                article_name = row['article_name']
                article_quantity = int(row['article_quantity'])
                article_price = float(row['article_price'])
                sku = row['SKU']

                article, _ = Article.objects.get_or_create(
                    name=article_name,
                    quantity=article_quantity,
                    price=article_price,
                    sku=sku,
                )
                sender_address, _ = Address.objects.get_or_create(address=sender_address)
                receiver_address, _ = Address.objects.get_or_create(address=receiver_address)
                carrier, _ = Carrier.objects.get_or_create(name=carrier)

                # Create the Shipment object
                shipment, _ = Shipment.objects.get_or_create(
                    tracking_number=tracking_number,
                    carrier=carrier,
                    sender_address=sender_address,
                    receiver_address=receiver_address,
                    article=article,
                )

        self.stdout.write(self.style.SUCCESS('Seed data inserted successfully.'))
