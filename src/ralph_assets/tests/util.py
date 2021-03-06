# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ralph_assets.models_assets import (
    Asset,
    AssetCategory,
    AssetCategoryType,
    AssetModel,
    AssetSource,
    AssetStatus,
    AssetType,
    AssetManufacturer,
    DeviceInfo,
    Warehouse
)

DEFAULT_ASSET_DATA = dict(
    manufacturer='Manufacturer1',
    model='Model1',
    warehouse='Warehouse',
    type=AssetType.data_center,
    status=AssetStatus.new,
    source=AssetSource.shipment,
    category='Category1',
)

SCREEN_ERROR_MESSAGES = dict(
    duplicated_sn_or_bc='Please correct duplicated serial numbers or barcodes.',  # noqa
    duplicated_sn_in_field='There are duplicate serial numbers in field.',
    contain_white_character="Serial number can't contain white characters.",
    django_required='This field is required.',
    count_sn_and_bc='Barcode list could be empty or must have the same number '
                    'of items as a SN list.',
    barcode_already_exist='Following barcodes already exists in DB: '
)


def create_manufacturer(name=DEFAULT_ASSET_DATA['manufacturer']):
    manufacturer, created = AssetManufacturer.objects.get_or_create(name=name)
    return manufacturer


def create_warehouse(name=DEFAULT_ASSET_DATA['warehouse']):
    warehouse, created = Warehouse.objects.get_or_create(name=name)
    return warehouse


def create_model(name=DEFAULT_ASSET_DATA['model'], manufacturer=None):
    """name = string, manufacturer = string"""
    if not manufacturer:
        manufacturer = create_manufacturer()
    else:
        manufacturer = create_manufacturer(manufacturer)
    model, created = AssetModel.objects.get_or_create(name=name)
    if created:
        model.manufacturer = manufacturer
        model.save()
    return model


def create_device(size=1):
    device = DeviceInfo(size=size)
    device.save()
    return device


def create_asset(sn, **kwargs):
    if not kwargs.get('type'):
        kwargs.update(type=DEFAULT_ASSET_DATA['type'])
    if not kwargs.get('model'):
        kwargs.update(model=create_model())
    if not kwargs.get('device_info'):
        kwargs.update(device_info=create_device())
    if not kwargs.get('status'):
        kwargs.update(status=DEFAULT_ASSET_DATA['status'])
    if not kwargs.get('source'):
        kwargs.update(source=DEFAULT_ASSET_DATA['source'])
    if not kwargs.get('support_period'):
        kwargs.update(support_period=24)
    if not kwargs.get('support_type'):
        kwargs.update(support_type='standard')
    if not kwargs.get('warehouse'):
        kwargs.update(warehouse=create_warehouse())
    kwargs.update(sn=sn)
    asset = Asset(**kwargs)
    asset.save()
    return asset


def create_category(type='data_center', name=DEFAULT_ASSET_DATA['category']):
    if type == 'back_office':
        type = AssetCategoryType.back_office
    elif type == 'data_center':
        type = AssetCategoryType.data_center
    category = AssetCategory()
    category.name = name
    category.type = type
    category.save()
    subcategory = AssetCategory()
    subcategory.name = 'Subcategory'
    subcategory.type = type
    subcategory.parent = category
    subcategory.save()
    return subcategory
