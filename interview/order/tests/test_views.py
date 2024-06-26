from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage
from interview.order.models import Order, OrderTag

class DeactivateOrderViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create necessary InventoryType and InventoryLanguage instances
        self.inventory_type = InventoryType.objects.create(name='Type1')
        self.inventory_language = InventoryLanguage.objects.create(name='English')

        # Create an Inventory instance
        self.inventory = Inventory.objects.create(
            name='Inventory 1',
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={}
        )

        # Create OrderTags
        self.tag1 = OrderTag.objects.create(name='Tag1')
        self.tag2 = OrderTag.objects.create(name='Tag2')

        # Create an Order instance
        self.order = Order.objects.create(
            inventory=self.inventory,
            start_date='2023-01-01',
            embargo_date='2023-06-01'
        )
        self.order.tags.add(self.tag1, self.tag2)

    def test_deactivate_order(self):
        # Make the POST request to deactivate the order
        url = reverse('deactivate-order', args=[self.order.id])
        response = self.client.post(url)

        # Refresh the order instance from the database
        self.order.refresh_from_db()

        # Check the response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the order is now inactive
        self.assertFalse(self.order.is_active)

    def test_deactivate_non_existent_order(self):
        # Make the POST request to deactivate a non-existent order
        url = reverse('deactivate-order', args=[9999])
        response = self.client.post(url)

        # Check the response status
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_deactivate_already_inactive_order(self):
        # Deactivate the order
        self.order.is_active = False
        self.order.save()

        # Make the POST request to deactivate the already inactive order
        url = reverse('deactivate-order', args=[self.order.id])
        response = self.client.post(url)

        # Refresh the order instance from the database
        self.order.refresh_from_db()

        # Check the response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the order remains inactive
        self.assertFalse(self.order.is_active)


class OrderListByDateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create necessary InventoryType and InventoryLanguage instances
        self.inventory_type = InventoryType.objects.create(name='Type1')
        self.inventory_language = InventoryLanguage.objects.create(name='English')

        # Create an Inventory instance
        self.inventory = Inventory.objects.create(
            name='Inventory 1',
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={}
        )

        # Create Orders
        self.order1 = Order.objects.create(
            inventory=self.inventory,
            start_date='2023-01-01',
            embargo_date='2023-06-01'
        )
        self.order2 = Order.objects.create(
            inventory=self.inventory,
            start_date='2023-07-01',
            embargo_date='2023-12-01'
        )

    def test_get_orders_within_date_range(self):
        url = reverse('order-list-by-date')
        response = self.client.get(url, {'start_date': '2023-01-01', 'embargo_date': '2023-06-30'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.order1.id)

    def test_get_orders_outside_date_range(self):
        url = reverse('order-list-by-date')
        response = self.client.get(url, {'start_date': '2024-01-01', 'embargo_date': '2024-12-31'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_orders_missing_date_parameters(self):
        url = reverse('order-list-by-date')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('start_date and embargo_date query parameters are required.', response.data['error'])