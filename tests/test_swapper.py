from django.test import TestCase
import swapper
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


import unittest

try:
    from django.db import migrations  # noqa
except ImportError:
    DJ17 = False
else:
    DJ17 = True


class SwapperTestCase(TestCase):

    # Tests that should work whether or not default_app.Type is swapped
    def test_fields(self):
        Type = swapper.load_model('default_app', 'Type')
        fields = dict(
            (field.name, field)
            for field in Type._meta.fields
        )
        self.assertIn('name', fields)

    def test_create(self):
        Type = swapper.load_model('default_app', 'Type')
        Item = swapper.load_model('default_app', 'Item')

        Item.objects.create(
            type=Type.objects.create(name="Type 1"),
            name="Item 1",
        )

        self.assertEqual(Item.objects.count(), 1)

        item = Item.objects.all()[0]
        self.assertEqual(item.type.name, "Type 1")

    def test_not_installed(self):
        Invalid = swapper.load_model("invalid_app", "Invalid", required=False)
        self.assertIsNone(Invalid)
        with self.assertRaises(ImproperlyConfigured):
            swapper.load_model("invalid_app", "Invalid", required=True)

    def test_non_contrib_app_split(self):
        self.assertEqual(swapper.split('alt_app.Type'), ('alt_app', 'Type'))

    def test_contrib_app_split(self):
        self.assertEqual(
            swapper.split('alt_app.contrib.named_things.NamedThing'),
            ('alt_app.contrib.named_things', 'NamedThing'))

    # Tests that only work if default_app.Type is swapped
    @unittest.skipUnless(settings.SWAP, "requires swapped models")
    def test_swap_setting(self):
        self.assertTrue(swapper.is_swapped("default_app", "Type"))
        self.assertEqual(
            swapper.get_model_name("default_app", "Type"),
            "alt_app.Type"
        )

    @unittest.skipUnless(settings.SWAP, "requires swapped models")
    def test_swap_fields(self):
        Type = swapper.load_model('default_app', 'Type')
        fields = dict(
            (field.name, field)
            for field in Type._meta.fields
        )
        self.assertIn('code', fields)

    @unittest.skipUnless(settings.SWAP, "requires swapped models")
    def test_swap_create(self):
        Type = swapper.load_model('default_app', 'Type')
        Item = swapper.load_model('default_app', 'Item')

        Item.objects.create(
            type=Type.objects.create(
                name="Type 1",
                code="type-1",
            ),
            name="Item 1",
        )

        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.all()[0]
        self.assertEqual(item.type.code, "type-1")

    @unittest.skipUnless(
        settings.SWAP and DJ17,
        "requires swapped models & Django 1.7"
    )
    def test_swap_dependency(self):
        self.assertEqual(
            swapper.dependency("default_app", "Type"),
            ("alt_app", "__first__")
        )

    # Tests that only work if default_app.Type is *not* swapped
    @unittest.skipIf(settings.SWAP, "requires non-swapped models")
    def test_default_setting(self):
        self.assertFalse(swapper.is_swapped("default_app", "Type"))
        self.assertEqual(
            swapper.get_model_name("default_app", "Type"),
            "default_app.Type"
        )

    @unittest.skipUnless(
        not settings.SWAP and DJ17,
        "requires non-swapped models & Django 1.7"
    )
    def test_default_dependency(self):
        self.assertEqual(
            swapper.dependency("default_app", "Type"),
            ("default_app", "__first__")
        )
