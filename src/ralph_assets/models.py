#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ajax_select import LookupChannel
from django.utils.html import escape
from django.db.models import Q

from ralph_assets.models_assets import (
    Asset,
    AssetCategory,
    AssetCategoryType,
    AssetManufacturer,
    AssetModel,
    AssetSource,
    AssetStatus,
    AssetType,
    DeviceInfo,
    LicenseType,
    OfficeInfo,
    PartInfo,
    Warehouse,
)
from ralph_assets.models_history import AssetHistoryChange
from ralph.discovery.models import Device


class DeviceLookup(LookupChannel):
    model = Asset

    def get_query(self, q, request):
        query = Q(
            Q(device_info__gt=0) & Q(
                Q(barcode__istartswith=q) |
                Q(sn__istartswith=q) |
                Q(model__name__icontains=q)
            )
        )
        return self.get_base_objects().filter(query).order_by('sn')[:10]

    def get_result(self, obj):
        return obj.id

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        return """
        <li class='asset-container'>
            <span class='asset-model'>%s</span>
            <span class='asset-barcode'>%s</span>
            <span class='asset-sn'>%s</span>
        </li>
        """ % (escape(obj.model), escape(obj.barcode or ''), escape(obj.sn))


class RalphDeviceLookup(LookupChannel):
    model = Device

    def get_query(self, q, request):
        query = Q(
            Q(
                Q(barcode__istartswith=q) |
                Q(id__istartswith=q) |
                Q(sn__istartswith=q) |
                Q(model__name__icontains=q)
            )
        )
        return Device.objects.filter(query).order_by('sn')[:10]

    def get_result(self, obj):
        return obj.id

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        return """
        <li class='asset-container'>
            <span class='asset-model'>%s</span>
            <span class='asset-barcode'>%s</span>
            <span class='asset-sn'>%s</span>
        </li>
        """ % (escape(obj.model), escape(obj.barcode or ''), escape(obj.sn))


class AssetLookup(LookupChannel):
    model = Asset

    def get_query(self, q, request):
        return Asset.objects.filter(
            Q(barcode__icontains=q) |
            Q(sn__icontains=q)
        ).order_by('sn', 'barcode')[:10]

    def get_result(self, obj):
        return obj.id

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        return '{}'.format(escape(unicode(obj)))


class AssetModelLookup(LookupChannel):
    model = AssetModel

    def get_query(self, q, request):
        return AssetModel.objects.filter(
            Q(name__icontains=q)
        ).order_by('name')[:10]

    def get_result(self, obj):
        return obj.name

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        return '{}'.format(escape(obj.name))


class AssetManufacturerLookup(LookupChannel):
    model = AssetModel

    def get_query(self, q, request):
        return AssetModel.objects.filter(
            Q(manufacturer__name__icontains=q)
        ).order_by('manufacturer__name')[:10]

    def get_result(self, obj):
        return obj.manufacturer.name

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        return '{}'.format(escape(obj.manufacturer.name))


class WarehouseLookup(LookupChannel):
    model = Warehouse

    def get_query(self, q, request):
        return Warehouse.objects.filter(
            Q(name__icontains=q)
        ).order_by('name')[:10]

    def get_result(self, obj):
        return obj.id

    def format_match(self, obj):
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        return escape(obj.name)


class DCDeviceLookup(DeviceLookup):
    def get_base_objects(self):
        return Asset.objects_dc


class BODeviceLookup(DeviceLookup):
    def get_base_objects(self):
        return Asset.objects_bo


__all__ = [
    'Asset',
    'AssetCategory',
    'AssetCategoryType',
    'AssetManufacturer',
    'AssetModel',
    'AssetSource',
    'AssetStatus',
    'AssetType',
    'DeviceInfo',
    'LicenseType',
    'OfficeInfo',
    'PartInfo',
    'Warehouse',
    'DeviceLookup',
    'DCDeviceLookup',
    'BODeviceLookup',
    'AssetModelLookup',
    'AssetHistoryChange',
]
