async def as_dict(obj):
    if isinstance(obj, list):
        for items in obj:
            for item in items:
                if isinstance(items[item], datetime.datetime):
                    items[item] = str(items[item])
                if isinstance(items[item], datetime.timedelta):
                    items[item] = str(items[item])
        return obj
    if isinstance(obj, dict):
        for item in obj:
            if isinstance(obj[item], datetime.datetime):
                obj[item] = str(obj[item])
            if isinstance(obj[item], datetime.timedelta):
                obj[item] = str(obj[item])
        return obj
    return obj
