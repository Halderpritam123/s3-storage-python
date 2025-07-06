def read_text_file(file_stream, page, limit):
    lines = file_stream.read().decode("utf-8").splitlines()

    total = len(lines)
    start = (page - 1) * limit
    end = start + limit

    return {
        "file_type": "text",
        "page": page,
        "limit": limit,
        "total_lines": total,
        "data": lines[start:end]
    }
