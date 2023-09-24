<h1>Image Upload API</h1>
<p>A simple Django Rest Framework-based API to upload and manage images by users.</p>

<h2>Features</h2>

<ul>
<li>User authentication and management.</li>
<li>Image upload with support for PNG and JPG formats.</li>
<li>Different user account tiers with various image access privileges.</li>
<li>Admin interface for user and account tier management.</li>
<li>Secure expiring links for image access.</li>
</ul>

<h2>Installation & Setup</h2>
<h3>Prerequisites</h3>

<ul>
<li>Docker</li>
<li>Git (for cloning the repository)</li>
<li>Postman (preferred for testing API)</li>
</ul>

<h2>Steps</h2>
Clone the repository:

```
git clone https://github.com/iCharliee/upload-and-list-images-api.git
```

Navigate to the project directory:

```
cd path/to/project
```

Run:

```
python manage.py makemigrations
python manage.py migrate
```

Build the docker-compose service:

```
docker-compose build
```

Run the service:

```
docker-compose up
```

<h2>Usage</h2>

<h3>Authorization!!!</h3>

<p>Project uses Basic Auth. Using Postman, before testing any HTTP request, go to "Authorization" section,
choose "Basic Auth" type and pass the credentials. There is already a superuser created with credentials:</p>

```
username: admin
password: admin
```

or using curl:

```
curl -X POST -u admin:admin ...
```

<h3>API Endpoints</h3>

<h3>1. Upload image endpoint</h2>

```
[POST] /api/upload/
```

<h4>Request example:</h4>

Using Postman:
<ol>
<li>Open Postman.</li>
<li>Set the request type to POST and enter the URL <b>http://127.0.0.1:8000/api/upload/</b>.</li>
<li>Under the "Body" tab, select "form-data".</li>
<li>In the "Key" column, type "uploaded_image". On the right side, you'll see a dropdown that says "Text". Click it and select "File".</li>
<li>Once "File" is selected, an input field with a "Select Files" button appears on the right. Click it and select your test.jpg file.</li>
<li>Send the request.</li>
</ol>

Using curl:

```
curl -X POST -F "uploaded_image=@path/to/test.jpg" http://127.0.0.1:8000/api/upload/
```

<h4>Response example:</h4>

```
{
    "id": 21,
    "uploaded_image": "http://127.0.0.1:8000/thumbnails/uploads/test.jpg",
    "thumbnail_200": "http://127.0.0.1:8000/thumbnails/thumbnails/test.jpg",
    "thumbnail_400": "http://127.0.0.1:8000/thumbnails/thumbnails/test_hbCEIP2.jpg"
}
```

<h3>2. List user's uploaded images endpoint</h2>

```
[GET] /api/list/
```

<h4>Response example:</h4>

```
[
    {
        "id": 3,
        "uploaded_image": "http://127.0.0.1:8000/thumbnails/uploads/test_dxthuBj.jpg",
        "thumbnail_200": "http://127.0.0.1:8000/thumbnails/thumbnails/test_B9FV4Im.jpg",
        "thumbnail_400": "http://127.0.0.1:8000/thumbnails/thumbnails/test_J73NCYB.jpg"
    },
    {
        "id": 4,
        "uploaded_image": "http://127.0.0.1:8000/thumbnails/uploads/test_OweS5S7.jpg",
        "thumbnail_200": "http://127.0.0.1:8000/thumbnails/thumbnails/test_bNhxkqh.jpg",
        "thumbnail_400": "http://127.0.0.1:8000/thumbnails/thumbnails/test_78zBq5D.jpg"
    },
    {
        "id": 5,
        "uploaded_image": "http://127.0.0.1:8000/thumbnails/uploads/test_La1ARSF.jpg",
        "thumbnail_200": "http://127.0.0.1:8000/thumbnails/thumbnails/test_qNJF2b7.jpg",
        "thumbnail_400": "http://127.0.0.1:8000/thumbnails/thumbnails/test_kh3nMHX.jpg"
    }
]
```

<h3>3. Fetch expiring link to the image</h3>

```
[GET] /api/get-expiring-link/<int:image_id>/
```

<h4>Response example:</h4>

```
{
    "url": "/thumbnails/uploads/test.jpg?token=1qkTdv"
}
```

<h2>Admin Interface</h2>

Navigate to http://localhost:8000/admin/ to access the Django admin interface. Use the credentials admin/admin for the default superuser.
