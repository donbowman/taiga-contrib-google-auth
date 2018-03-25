Taiga contrib google auth
=========================

A Taiga plugin for google oauth2 authentication (Ported from official gitlab auth).

Installation
------------
### Production env

#### Taiga Back

In your Taiga back python virtualenv install the pip package `taiga-contrib-google-auth` with:

```bash
  pip install taiga-contrib-google-auth
```

Modify your `settings/local.py` and include the line:

```python
    INSTALLED_APPS += ["taiga_contrib_google_auth"]

    # Get these from https://console.cloud.google.com/apis/credentials

    GOOGLE_API_CLIENT_ID = env("GOOGLE_API_CLIENT_ID")
    GOOGLE_API_CLIENT_SECRET = env("GOOGLE_API_CLIENT_SECRET")
    GOOGLE_API_REDIRECT_URI = env("GOOGLE_API_REDIRECT_URI")
    GOOGLE_RESTRICT_LOGIN = [env("GOOGLE_RESTRICT_LOGIN")]
    GOOGLE_API_ALLOW_DOMAIN = [env("GOOGLE_API_ALLOW_DOMAIN")]
```

#### Taiga Front

Download in your `dist/plugins/` directory of Taiga front the `taiga-contrib-google-auth` compiled code:

```bash
  cd dist/
  mkdir -p plugins/google-auth
  cd plugins/google-auth
  (clone front/dist dir here)
```

Include in your `dist/conf.json` in the 'contribPlugins' list the value `"/plugins/google-auth/google-auth.json"`:

```json
...
    "googleClientId": "YOUR-GOOGLE-CLIENT-ID",
    "contribPlugins": [
        (...)
        "/plugins/google-auth/google-auth.json"
    ]
...
```

### Dev env

#### Taiga Back

Clone the repo and

```bash
  cd taiga-contrib-google-auth/back
  workon taiga
  pip install -e .
```

Modify `taiga-back/settings/local.py` and include the line:

```python
    INSTALLED_APPS += ["taiga_contrib_google_auth"]

    # Get these from https://console.cloud.google.com/apis/credentials

    GOOGLE_API_CLIENT_ID = env("GOOGLE_API_CLIENT_ID")
    GOOGLE_API_CLIENT_SECRET = env("GOOGLE_API_CLIENT_SECRET")
    GOOGLE_API_REDIRECT_URI = env("GOOGLE_API_REDIRECT_URI")
    GOOGLE_RESTRICT_LOGIN = [env("GOOGLE_RESTRICT_LOGIN")]
    GOOGLE_API_ALLOW_DOMAIN = [env("GOOGLE_API_ALLOW_DOMAIN")]
```

#### Taiga Front

After clone the repo link `dist` in `taiga-front` plugins directory:

```bash
  cd taiga-front/dist
  mkdir -p plugins
  cd plugins
  ln -s ../../../taiga-contrib-google-auth/front/dist google-auth
```

Include in your `dist/conf.json` in the 'contribPlugins' list the value `"/plugins/google-auth/google-auth.json"`:

```json
...
    "googleClientId": "YOUR-GOOGLE-CLIENT-ID",
    "contribPlugins": [
        (...)
        "/plugins/google-auth/google-auth.json"
    ]
...
```

In the plugin source dir `taiga-contrib-google-auth/front` run

```bash
npm install
```
and use:

- `gulp` to regenerate the source and watch for changes.
- `gulp build` to only regenerate the source.

Running tests
-------------

We only have backend tests, you have to add your `taiga-back` directory to the
PYTHONPATH environment variable, and run py.test, for example:

```bash
  cd back
  add2virtualenv /home/taiga/taiga-back/
  py.test
```
