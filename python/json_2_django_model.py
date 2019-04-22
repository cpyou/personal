def camel2underscore(jsondata):
    import re
    result = {}
    for (k, v) in jsondata.items():
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', k)
        k = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        result[k] = camel2underscore(v) if isinstance(v, dict) else v
    return result


def json_2_django_model(json_data):
    field_map = {
        str: "CharField(max_length=128)",
        int: "IntegerField(default=0)",
        float: "FloatField(default=0.0)",
        bool: "BooleanField(default=False)",
    }
    for field, v in camel2underscore(json_data).items():
        filed_type = field_map.get(type(v), str)
        print(f'{field} = models.{filed_type}')

d = {'TestName': 'test name', 'TestInt': 1, 'TestFloat': 1.0, 'TestBool': True}
json_2_django_model(d)
