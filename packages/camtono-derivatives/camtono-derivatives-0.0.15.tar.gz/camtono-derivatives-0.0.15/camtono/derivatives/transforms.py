def distinct_function(value, data_type, **kwargs):
    return dict(distinct=[value]), data_type


def min_function(value, data_type, **kwargs):
    return dict(min=value), data_type


def max_function(value, data_type, **kwargs):
    return dict(max=value), data_type


def avg_function(value, data_type, **kwargs):
    return dict(avg=value), data_type


def count_function(value, **kwargs):
    return dict(count=value), 'INT64'


def array_agg_function(value, data_type, order_by, **kwargs):
    # TODO array agg inputs
    resp = dict(array_agg=dict(value=value))
    new_data_type = 'ARRAY<{}>'.format(data_type)
    if kwargs.get('order_by'):
        resp['array_agg']['orderby'] = order_by
    return resp, new_data_type


def get_transform_function(name):
    import importlib
    return getattr(importlib.import_module('camtono.derivatives.transforms'), "{}_function".format(name))


def apply_transforms(value, data_type: str, transforms: list):
    for transform in reversed(transforms):
        f = get_transform_function(name=transform['name'])
        value, data_type = f(value=value, data_type=data_type, inputs=transform.get('inputs', dict()))
    return value, data_type


def check_transforms_for_aggregation_functions(transforms):
    aggregates = {'count', 'min', 'max', 'avg'}
    aggregations = [i for i in transforms if i['name'] in aggregates]
    return True if aggregations else False
