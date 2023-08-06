def generate_select_mapping(default_inputs, definition_outputs, output_queries, input_features, grain,
                            feature_map) -> tuple:
    from camtono.derivatives.transforms import check_transforms_for_aggregation_functions
    filter_select = generate_filter_select(definition_outputs=definition_outputs,
                                           feature_map=feature_map, grain=grain)
    feature_outputs = generate_feature_select(feature_map=feature_map, default_inputs=default_inputs)
    select_mapping = dict(
        filter=filter_select,
        final=generate_final_select(filter_select=filter_select, feature_outputs=feature_outputs,
                                    definition_outputs=definition_outputs, input_features=input_features),
        **feature_outputs
    )
    group_by = dict(final=[idx + 1 for idx, i in enumerate(definition_outputs)
                           if not check_transforms_for_aggregation_functions(transforms=i.get('transforms', []))])
    return select_mapping, {k: v for k, v in group_by.items() if
                            select_mapping.get(k) and len(v) != len(select_mapping[k])}


def extract_select_schema(select):
    return [dict(type=i['type'], name=i['name']) for i in select]


def extract_select_output(select):
    return [dict(value=i['value'], name=i['name']) for i in select]


def generate_filter_select(definition_outputs, grain, feature_map):
    filter_select = []
    common_output = identify_common_output(features=list(feature_map.values()), grain=grain)
    for output in [i for i in definition_outputs if 'feature_id' not in i.keys()]:
        if 'value' in output.keys():
            continue
        elif output['column_name'] not in common_output.keys():
            raise ValueError("{} is not shared by all features".format(output['column_name']))
        else:
            filter_select.append(
                dict(
                    name=output['column_name'],
                    value='t0.{}'.format(output['column_name']),
                    type=common_output[output['column_name']]['data_type']
                )
            )
    if grain not in [i['name'] for i in filter_select]:
        filter_select = [
            dict(
                name=grain,
                value='t0.{}'.format(grain),
                type=common_output[grain]['type'] if grain in common_output.keys() else common_output['grain'][
                    'data_type']
            ), *filter_select]
    return filter_select


def identify_common_output(features, grain):
    common_output = None
    feature = dict(outputs=[])
    for feature in features:
        if common_output is None:
            common_output = set([i['display_name'] for i in feature['outputs']])
        common_output.intersection_update(set([i['display_name'] for i in feature['outputs']]))
    common_output_dict = dict()

    for output in feature['outputs']:
        if output['display_name'] in common_output:
            common_output_dict[output['display_name']] = output
        if output['display_name'] == '{grain}':
            common_output_dict[grain] = output
            common_output_dict[grain]['name'] = common_output_dict[grain]['name'].format(grain=grain)
            common_output_dict[grain]['display_name'].format(grain=grain)
    return common_output_dict


def generate_final_select(filter_select, definition_outputs, feature_outputs, input_features):
    from camtono.derivatives.transforms import apply_transforms
    final_select = []
    filter_select_dict = {i['name']: i for i in filter_select}
    for output in definition_outputs:
        if output['column_name'] in filter_select_dict:
            column_value = 'base.{}'.format(output['column_name'])
            data_type = filter_select_dict[output['column_name']]['type']
        elif 'feature_id' in output.keys():
            output_types = {i['name']: i['type'] for i in feature_outputs[output['feature_id']]}
            table_name = "sub_feature_{idx}".format(idx=list(feature_outputs.keys()).index(output['feature_id']))
            if not input_features and table_name == 'sub_feature_0':
                table_name = 'base'
            column_value = '{table_name}.{column}'.format(
                column=output['column_name'],
                table_name=table_name)
            data_type = output_types[output['column_name']]
        elif 'value' in output.keys():
            column_value = 'sub_feature_{idx}.{column}'.format(
                column=output['column_name'],
                idx=list(feature_outputs.keys()).index(output['feature_id']))
            data_type = type(output['value'])
        else:
            raise ValueError('Output must reference a feature or have a defined value')
        column_value, data_type = apply_transforms(value=column_value, data_type=data_type,
                                                   transforms=output.get('transforms', []))
        final_select.append(
            dict(
                name=output['rename_as'] if 'rename_as' in output.keys() else output['column_name'],
                value=column_value,
                type=data_type
            ),
        )

    return final_select


def generate_feature_select(feature_map, default_inputs) -> dict:
    feature_selects = dict()
    for feature_id, feature in feature_map.items():
        feature_selects[feature_id] = [
            dict(
                name=output['display_name'].format(**default_inputs),
                value=output['name'].format(**default_inputs),
                type=output['data_type']
            )
            for output in feature['outputs']
        ]
    return feature_selects
