import csv
import uuid
import os


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from collections import Counter



@csrf_exempt
def upload_csv_file(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=400)

    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file uploaded'}, status=400)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        return JsonResponse({'error': 'Only CSV files are allowed'}, status=400)

    upload_dir = os.path.join(settings.BASE_DIR, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)

    dataset_id = str(uuid.uuid4())[:8]
    file_path = os.path.join(upload_dir, f'{dataset_id}.csv')

    with open(file_path, 'wb+') as destination:
        for chunk in csv_file.chunks():
            destination.write(chunk)

    try:
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

            if len(rows) == 0:
                return JsonResponse({'error': 'CSV file is empty'}, status=400)

            header = rows[0]
            if len(header) == 0:
                return JsonResponse({'error': 'CSV has no columns'}, status=400)

    except Exception:
        return JsonResponse({'error': 'Invalid CSV file'}, status=400)

    column_types = {}
    try:
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for col in header:
                numeric_count = 0
                total = 0
                for row in reader:
                    value = row.get(col)
                    if value:
                        total += 1
                        try:
                            float(value)
                            numeric_count += 1
                        except:
                            pass
                column_types[col] = 'numeric' if numeric_count > total / 2 else 'text'
                f.seek(0)
                next(reader)
    except Exception:
        return JsonResponse({'error': 'Error while reading CSV data'}, status=400)

    return JsonResponse({
        'dataset_id': dataset_id,
        'columns': column_types
    })


def fetch_dataset_table(request, dataset_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed'}, status=400)

    file_path = os.path.join(settings.BASE_DIR, 'uploads', f'{dataset_id}.csv')

    if not os.path.exists(file_path):
        return JsonResponse({'error': 'Dataset not found'}, status=404)

    try:
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            columns = reader.fieldnames
    except Exception:
        return JsonResponse({'error': 'Error reading CSV file'}, status=400)

    return JsonResponse({
        'columns': columns,
        'rows': rows
    })

def calculate_column_statistics(request, dataset_id, column_name):
    if request.method != "GET":
        return JsonResponse({"error": "Only GET method allowed"}, status=400)

    csv_path = os.path.join(settings.BASE_DIR, "uploads", f"{dataset_id}.csv")

    if not os.path.exists(csv_path):
        return JsonResponse({"error": "Dataset not found"}, status=404)

    numeric_values = []
    numeric_mode_values = []
    categorical_values = []
    missing_count = 0

    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        if column_name not in reader.fieldnames:
            return JsonResponse({"error": "Column not found"}, status=404)

        for row in reader:
            value = row.get(column_name)

            if value is None or value.strip() == "":
                missing_count += 1
                continue

            # store categorical value
            categorical_values.append(value)

            # try numeric conversion
            try:
                num_val = float(value)
                numeric_values.append(num_val)
                numeric_mode_values.append(num_val)
            except ValueError:
                pass

    # ---------- Numeric calculations ----------
    min_val = max_val = mean_val = median_val = None

    if numeric_values:
        numeric_values.sort()
        count = len(numeric_values)

        min_val = numeric_values[0]
        max_val = numeric_values[-1]
        mean_val = sum(numeric_values) / count

        if count % 2 == 0:
            median_val = (numeric_values[count // 2 - 1] + numeric_values[count // 2]) / 2
        else:
            median_val = numeric_values[count // 2]

    # ---------- Mode calculation ----------
    mode_values = []

    if numeric_mode_values:
        freq_map = Counter(numeric_mode_values)
    else:
        freq_map = Counter(categorical_values)

    if freq_map:
        highest_freq = max(freq_map.values())
        mode_values = [val for val, cnt in freq_map.items() if cnt == highest_freq]

    return JsonResponse({
        "column": column_name,
        "min": min_val,
        "max": max_val,
        "mean": mean_val,
        "median": median_val,
        "mode": mode_values,
        "missing_values": missing_count
    })

    

def generate_column_histogram(request, dataset_id, column_name):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET method allowed'}, status=400)

    file_path = os.path.join(settings.BASE_DIR, 'uploads', f'{dataset_id}.csv')

    if not os.path.exists(file_path):
        return JsonResponse({'error': 'Dataset not found'}, status=404)

    numeric_data = []

    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        if column_name not in reader.fieldnames:
            return JsonResponse({'error': 'Column not found'}, status=404)

        for row in reader:
            value = row.get(column_name)
            if value is None or value.strip() == '':
                continue
            try:
                numeric_data.append(float(value))
            except ValueError:
                continue

    if len(numeric_data) == 0:
        return JsonResponse({'error': 'Histogram available only for numeric columns'}, status=400)

    minimum_value = min(numeric_data)
    maximum_value = max(numeric_data)

    bin_count = 30
    bin_size = (maximum_value - minimum_value) / bin_count

    histogram_bins = []
    for i in range(bin_count):
        start = minimum_value + i * bin_size
        end = start + bin_size
        histogram_bins.append({
            'range': f'{round(start,2)} - {round(end,2)}',
            'count': 0
        })

    for value in numeric_data:
        index = int((value - minimum_value) / bin_size)
        if index == bin_count:
            index -= 1
        histogram_bins[index]['count'] += 1

    return JsonResponse({
        'column': column_name,
        'bins': histogram_bins
    })

def home(request):
    return render(request, 'index.html')







