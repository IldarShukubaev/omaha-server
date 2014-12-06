# coding: utf8

"""
This software is licensed under the Apache 2 license, quoted below.

Copyright 2014 Crystalnix Limited

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this file except in compliance with the License. You may obtain a copy of
the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.
"""

from django import forms
from django_select2 import Select2Widget
from crash.models import Symbols
from models import Crash


class CrashFrom(forms.ModelForm):
    class Meta:
        model = Crash
        exclude = []


class SymbolsAdminForm(forms.ModelForm):
    class Meta:
        model = Symbols
        exclude = []
        widgets = {
            'version': Select2Widget(attrs={'style': 'width:300px'},
                                     select2_options={'minimumResultsForSearch': 2}),
        }
