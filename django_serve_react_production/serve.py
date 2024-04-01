# A way to test a production build on Windows
# This relies on Django to provide static files,
# which is not recommended for large-scale applications.
# For production, use a web server like Nginx or Apache.

from waitress import serve
from django_serve_react.wsgi import application

if __name__ == '__main__':
    print('Serving React-Django Production Build on http://localhost:8000')
    serve(application, host='0.0.0.0', port=8000)
    