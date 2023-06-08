from io import StringIO
import csv
from .models import Category


def convert_to_csv(data, fieldnames):
    filename = 'data.csv'

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for item in data:
            writer.writerow({
                fieldname: getattr(item, fieldname) for fieldname in fieldnames
            })

    return filename


def convert_set_to_csv(queryset, fieldnames):
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for obj in queryset:
        row = {field: getattr(obj, field) for field in fieldnames}
        writer.writerow(row)

    return output.getvalue()


def process_category(category_name, custom_category, user):
    category = None

    if custom_category:
        category, _ = Category.objects.get_or_create(
            name=custom_category, user=user)
    elif category_name:
        category, _ = Category.objects.get_or_create(
            name=category_name, user=user)

    return category
    