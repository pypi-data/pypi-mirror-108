# Django URL Prefixer
A Django middleware that prepends some text/link to every relative link before rendering a template.

Therefore, relative link inside a template whether it be a HTML or JavaScript file will have some defined text prepended.

This will only affective relative links and and will not update absolute links. Examples of the how the middleware will affect the links are below when we add
the prefix `example.com` to each link:
| Original                | With Middleware                     |
| ----------------------- | ----------------------------------- |
| `/download`             | `example.com/download`              |
| `example.com/something` | `example.com/something` (no change) |
| `/`                     | `example.com/something`             |

## Use Cases
This is useful for when you need to append a prefix to all links within the templates including static assets.

When this is not required, alternative options include adding the prefix directly to the path in your URLs config are viable.

This was built with the idea of having multiple Django applications on the same server all be accessible via a single port.

Normally, if you want to achieve something similar to this, you would have different applications available on different ports. And so you would have an architecture that looks like the following:

![Architecture without middleware](https://raw.githubusercontent.com/Salaah01/django-url-prefixer/master/examples/without_middleware.png)

Therefore, where the domain is iamsalaah.com, in order to access the main portfolio site, the user would to navigate to iamsalaah.com which is fine as it is served on ports 80/443.

But, in order to access Project 1, the user would need to navigate to iamsalaah.com:8001/ and similarly, if they want to access Project 2, they would need to navigate to iamsalaah.com:8002/. Suddenly (at least for me) this starts to look not too great.

So, for my own use case, I have Dockerised all the Django projects and have them up and running, each of which are exposing port 80. For the sake of this example, we will imagine there are two projects, and the network names of each of these projects are called `project_1_network` and `project_2_network`. Similarly, the web server services for projects 1 and 2 will be called `project_1_nginx` and `project_2_nginx` respectively.

I would then ensure that my portfolio site's web server container have access to both `project_1_network` and `project_2_network` and would create a something similar to the following configurations (Nginx).
```nginx
server {
  listen 443 ssl http2;
  listen [::]:443 ssl http2;

  location / {
    # Let's imagine that the main portfolio site is running on port 8000.
    proxy_pass http://portfolio_site:8000;  
  }

  location /projects/project-1/site/ {
    rewrite ^/projects/project-1/site(.*) /$1 break;
    proxy_pass project_1_nginx;
  }

  location /projects/project-2/site/ {
    rewrite ^/projects/project-2/site(.*) /$1 break;
    proxy_pass project_2_nginx;
  }
}
```

This configuration would create the following architecture:

![Architecture with middleware](https://raw.githubusercontent.com/Salaah01/django-url-prefixer/master/examples/with_middleware.png)

Therefore, rather then having different ports appearing in the URL, if the user access `https://iamsalaah.com/` they would be taken to the main portfolio site as normal. But, if they access `https://iamsalaah.com/projects/project-1/site`, they `project_1_nginx` webserver will handle the request and show Project 1.
Similarly, if the user were to access `https://iamsalaah.com/projects/site/page-3`, the webserver (`project_2_nginx`) would return `/page-3` from Project 3.

The reason including the middleware is to support this behaviour, as we can set the `URL_PREFIXER` to equal to `projects/project-1/site` and `projects/project-2/site` in the Project 1 and 2 settings respectively.

This would mean that, if the user is currently access Project 2's index, and that page has a link to `page-1`, where the link would normally appear as `/page-1`, this will be replaced with `projects/project-1/site/page-1`. This would be served by the portfolio's webserver and not the webserver belonging Project 1. Therefore, in this case, the user would be navigated to `iamsalaah.com/page-1`.

By including and configuring the middleware, we can now navigate the to `iamsalaah.com/projects/project-1/site/page-1` which would be served by Project 1's webserver.

## Setup
### Add to Installed Apps
Add `django_url_prefixer` to your `INSTALLED_APPS` in your settings:
```python
INSTALLED_APPS = [
  # ...,
  'django_url_prefixer'
]
```

### Enable Middleware
To enable to middleware, add to the end of your `MIDDLEWARE` in your settings:
```python
MIDDLEWARE = [
  # ...,
  'django_url_prefixer.middleware.URLPrefixer
]
```

### Configure URL Prefixer
Add a `URL_PREFIXER` variable to your settings with text you want to prefix all
URLs with.
```python
URL_PREFIXER = 'prefix_text'
```
This will in turn update all relative links so that they being with `prefix_text`.
