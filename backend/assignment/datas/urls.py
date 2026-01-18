from django.urls import path
from .views import (
    upload_csv_file,
    fetch_dataset_table,
    calculate_column_statistics,
    generate_column_histogram,
    home
    
)

urlpatterns = [
    path('', home),
    path('upload/', upload_csv_file),
    path('dataset/<str:dataset_id>/table/', fetch_dataset_table),
    path('dataset/<str:dataset_id>/column/<str:column_name>/stats/', calculate_column_statistics),
    path('dataset/<str:dataset_id>/column/<str:column_name>/histogram/', generate_column_histogram),

]
