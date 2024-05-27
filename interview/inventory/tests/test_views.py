# interview/inventory/tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage
from interview.inventory.serializers import InventorySerializer

class InventoryListAfterDateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create some InventoryType and InventoryLanguage instances
        self.inventory_type = InventoryType.objects.create(name='Type1')
        self.inventory_language = InventoryLanguage.objects.create(name='English')

        # Create inventory items
        self.inventory1 = Inventory.objects.create(
            name='Inventory 1',
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={}
        )
        self.inventory2 = Inventory.objects.create(
            name='Inventory 2',
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={}
        )

        # Set different creation dates
        self.inventory1.created_at = datetime.now() - timedelta(days=5)
        self.inventory1.save()
        self.inventory2.created_at = datetime.now() - timedelta(days=1)
        self.inventory2.save()

    def test_get_inventory_after_date(self):
        # Define the date for filtering
        filter_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')

        # Make the GET request with the date query parameter
        response = self.client.get(reverse('inventory-created-after'), {'date': filter_date})

        # Deserialize the response data
        expected_data = InventorySerializer([self.inventory2], many=True).data

        # Check the response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the response data
        self.assertEqual(response.data, expected_data)

    def test_get_inventory_after_date_invalid_format(self):
        # Make the GET request with an invalid date format
        response = self.client.get(reverse('inventory-created-after'), {'date': 'invalid-date'})

        # Check the response status
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check the error message
        self.assertIn('Invalid date format. Use YYYY-MM-DD.', response.data['error'])

    def test_get_inventory_after_date_missing_parameter(self):
        # Make the GET request without the date query parameter
        response = self.client.get(reverse('inventory-created-after'))

        # Check the response status
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check the error message
        self.assertIn('Date query parameter is required', response.data['error'])
