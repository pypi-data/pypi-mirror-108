import dash_html_components as html
import dash_devextreme as ddx

from django.test import TestCase
from django import forms

from dash_ddx_catalog.forms import DashDDXForm


class SimpleForm(DashDDXForm):
    name = forms.CharField(label='Test label', max_length=255)


class TestDashDDXForm(TestCase):
    def test_simple(self):
        fields = SimpleForm(initial=dict(name='Test', name2='Test2')).as_ddx_div()

        self.assertTrue(fields[0].__class__ is html.Div)
        self.assertTrue(fields[0].children[0].__class__ is html.Span)
        self.assertTrue(fields[0].children[1].__class__ is ddx.TextBox)
        self.assertTrue(fields[0].children[1].name == 'name')
        # self.assertTrue(fields[0].children[1].value == 'Test')
        # self.assertTrue(fields[0].children[1].maxLength == 255)
