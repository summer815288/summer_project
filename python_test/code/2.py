import base64

with open('/Users/edz/Documents/pongo/python_test/code/1.jpg', 'rb') as f:
    base64_data = base64.b64encode(f.read())
    print(base64_data)
    b64 = base64_data.decode()
    print(b64)
