import base64

def read_image_file(file_stream):
    encoded_string = base64.b64encode(file_stream.read()).decode('utf-8')
    return {
        "file_type": "image",
        "base64": f"data:image/png;base64,{encoded_string}"
    }
