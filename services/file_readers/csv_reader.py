import csv
from io import StringIO

def read_csv_file(file_stream, page, limit):
    content = file_stream.read().decode("utf-8")
    csv_data = csv.reader(StringIO(content))

    rows = list(csv_data)
    header = rows[0]
    data_rows = rows[1:]

    total = len(data_rows)
    start = (page - 1) * limit
    end = start + limit

    return {
        "file_type": "csv",
        "page": page,
        "limit": limit,
        "total_rows": total,
        "columns": header,
        "data": [dict(zip(header, row)) for row in data_rows[start:end]]
    }
