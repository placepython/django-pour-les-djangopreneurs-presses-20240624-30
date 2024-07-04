# Compilation of your frontend assets

This folder manage the construction of your static assets using the Vite build tool. The current README helps you getting started with this process. Read it carefully.

## Node.js

As a prerequisite, you will need npm to install frontend your dependencies and launch the commands. Hence, building your frontend static assets using this folder requires you to install Node.js globally on your computer. You can do this by [downloading the appropriate installer](https://nodejs.org/en/download/current) for your operating system. This is the very first step of your journey.

## Installing your project frontend dependencies

The first step to build your static files is to install frontend dependencies in the current folder. The npm package management has been designed exactly for this task. It will be used to install all the tools and libraries listed in your package.json package-lock.json files. 

Execute the following command to create automatically a node_modules subfolder with all your project frontend dependencies inside:

```
$ npm install
```

## Developing your frontend with the Vite build tool

### Running vite for development

For development purpose, you can start the frontend development server by running the command `$ npm start` from the current directory. This command will launch the vite dev server and recompile your static assets each time a file update is detected. It will therefore block and observe your filesystem until you stop it using CTRL+C.

### Generating your production static files

To generate your static files for deployment, use the command `$ npm run build`. It will compile and optimize your assets and store them in the static folder of your django project.

## Use Django-vite in your Django project

On the django side, using the django-vite package is a valuable option. You can install it using pipenv (or pip if you prefer) like this:

```bash
$ pip install django-vite
```
or 
```bash
$ pipenv install django-vite
```

Once installed, add `django_vite` in the INSTALLED_APPS list of your django settings. Then, configure it using the
DJANGO_VITE variable in your settings:

```python
DJANGO_VITE = {
    "default": {
        "dev_mode": DEBUG,
    },
}
```

Then add the <path to frontend>/dist/ folder to the STATICFILES_DIRS:

```python
STATICFILES_DIRS = [
    BASE_DIR / "frontend" / "dist"
]
```

In your templates, you need to use django-vite to reference your assets:

```
{% load django_vite %}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page title</title>

    {% vite_hmr_client %}
    {# path of your vite assets are relative to the frontend directory #}
    {% vite_asset 'src/application/app.js' %}
</head>
<body>
    ...
</body>
</html>
```

You can also use the `{% vite_asset_url %}` tag to get the get the url of a static
ressource handled by vite:

```html
<img src="{% vite_asset_url 'path/to/my/image.png' %}" alt="the python logo" />
```

For more information on django-vite, feel free to read the [offical README for the project](https://github.com/MrBin99/django-vite/blob/3.0.0/README.md).

## Using django-browser-reload to refresh your web browser

Vite is very smart in refreshing your web browser with javascript or CSS code changes in the current folder. If you want to issue an automatic refresh also when your templates or views are modified, the [django-browser-reload package](https://github.com/adamchainz/django-browser-reload) is a valuable and simple option.

You can install django-browser-reload as simply using pipenv (or pip if you prefer):

```
$ pipenv install django-browser-reload
```

The [documentation of this package](https://github.com/adamchainz/django-browser-reload/blob/main/README.rst) provide good explanations about the configuration in your django settings file.

Here is the procedure:

1. Ensure you have `django.contrib.staticfiles` in your INSTALLED_APPS.
2. Add django-browser-reload to your INSTALLED_APPS: 
```python
INSTALLED_APPS = [
    ...,
    "django_browser_reload",
    ...,
]
```
3. Include the app URLs in your root URLconf:
```python
from django.urls import include, path

urlpatterns = [
    ...,
    path("__reload__/", include("django_browser_reload.urls")),
]
```
You can use another prefix if required.

5. Add the middleware:
```python
MIDDLEWARE = [
    # ...
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    # ...
]
```
The middleware should be listed after any others that encode the response, such as Django’s GZipMiddleware.

The middleware automatically inserts the required script tag on HTML responses before </body> when DEBUG is True. It does so to every HTML response, meaning it will be included on Django’s debug pages, admin pages, etc. If you want more control, you can instead insert the script tag in your templates (see the official documentation).

