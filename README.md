**Tech Stack**
    > Backend: Python 3, Django, Django REST–style APIs
    > Frontend: HTML5, CSS3, Vanilla JavaScript (Fetch API)
**Setup & Run Instructions (Local)**
    > Navigate to the project root directory:
    > DromoLys_FullStack_Assignment
Activate the virtual environment named env:
    > env\Scripts\activate
Navigate to the backend project directory:
    > cd backend
    > cd assignment
Run the following Django commands:
    > python manage.py makemigrations
    > python manage.py migrate
    > python manage.py runserver
Open the application in the browser and upload CSV files using : 
    > http://127.0.0.1:8000/api/

**API Endpoints Implemented**
-------------------------
> Upload CSV File
Endpoint: /api/upload/
Method: POST
Description: Uploads a CSV file and stores it on the server. Returns a unique dataset_id for further operations.

> View Uploaded Dataset as Table
Endpoint: /api/dataset/<dataset_id>/table/
Method: GET
Description: Returns column names and rows of the uploaded CSV file for rendering as a table in the UI.
> Column Statistics
Endpoint: /api/dataset/<dataset_id>/column/<column_name>/stats/
Method: GET
Description: Computes statistics for a selected column.
Numeric columns: min, max, mean, median, mode
Categorical columns: mode
Missing/invalid values are ignored in numeric calculations and reported separately.

> Column Histogram
Endpoint: /api/dataset/<dataset_id>/column/<column_name>/histogram/
Method: GET
Description: Generates histogram data for numeric columns using fixed bins. Returns a clear error message if the column is non-numeric or contains no valid numeric data.
