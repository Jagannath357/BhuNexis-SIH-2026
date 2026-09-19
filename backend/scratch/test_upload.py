import urllib.request
import json

# 1. Login
login_data = json.dumps({'email': 'officer@bhunexis.demo', 'password': 'password123', 'role': 'REVENUE_OFFICER'}).encode()
req = urllib.request.Request('http://127.0.0.1:8000/api/v1/auth/login', data=login_data, headers={'Content-Type': 'application/json'})
token = json.loads(urllib.request.urlopen(req).read().decode())['access_token']
print("Officer authenticated successfully!")

# 2. Upload Document
boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
body = (
    f'--{boundary}\r\n'
    'Content-Disposition: form-data; name="file"; filename="sample_land_record.png"\r\n'
    'Content-Type: image/png\r\n\r\n'
    'fake_image_bytes_for_land_record_test\r\n'
    f'--{boundary}--\r\n'
).encode('utf-8')

req_upload = urllib.request.Request(
    'http://127.0.0.1:8000/api/v1/documents',
    data=body,
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': f'multipart/form-data; boundary={boundary}'
    }
)

res = urllib.request.urlopen(req_upload)
result = json.loads(res.read().decode())
print("Upload API Success Response:", result)
