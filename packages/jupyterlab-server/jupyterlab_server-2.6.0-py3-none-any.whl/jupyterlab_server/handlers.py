# coding: utf-8
"""JupyterLab Server handlers"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
from urllib.parse import urlparse

from tornado import template, web

from jupyter_server.extension.handler import ExtensionHandlerMixin, ExtensionHandlerJinjaMixin

from .config import LabConfig, get_page_config, recursive_update
from .listings_handler import ListingsHandler, fetch_listings
from .server import FileFindHandler, JupyterHandler
from .server import url_path_join as ujoin
from .settings_handler import SettingsHandler
from .themes_handler import ThemesHandler
from .translations_handler import TranslationsHandler
from .workspaces_handler import WorkspacesHandler
from .licenses_handler import LicensesHandler, LicensesManager

# -----------------------------------------------------------------------------
# Module globals
# -----------------------------------------------------------------------------

MASTER_URL_PATTERN = '/(?P<mode>{}|doc)(?P<workspace>/workspaces/[a-zA-Z0-9\-\_]+)?(?P<tree>/tree/.*)?'

DEFAULT_TEMPLATE = template.Template("""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Error</title>
</head>
<body>
<h2>Cannot find template: "{{name}}"</h2>
<p>In "{{path}}"</p>
</body>
</html>
""")


def is_url(url):
  """Test whether a string is a full url (e.g. https://nasa.gov)

  https://stackoverflow.com/a/52455972
  """
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False



class LabHandler(ExtensionHandlerJinjaMixin, ExtensionHandlerMixin, JupyterHandler):
    """Render the JupyterLab View."""

    @web.authenticated
    @web.removeslash
    def get(self, mode = None, workspace = None, tree = None):
        """Get the JupyterLab html page."""
        workspace = 'default' if workspace is None else workspace.replace('/workspaces/','')
        tree_path = '' if tree is None else tree.replace('/tree/','')

        self.application.store_id = getattr(self.application, 'store_id', 0)
        config = LabConfig()
        app = self.extensionapp
        settings_dir = app.app_settings_dir

        # Handle page config data.
        page_config = self.settings.setdefault('page_config_data', {})
        terminals = self.settings.get('terminals_available', False)
        server_root = self.settings.get('server_root_dir', '')
        server_root = server_root.replace(os.sep, '/')
        base_url = self.settings.get('base_url')

        # Remove the trailing slash for compatibiity with html-webpack-plugin.
        full_static_url = self.static_url_prefix.rstrip('/')
        page_config.setdefault('fullStaticUrl', full_static_url)

        page_config.setdefault('terminalsAvailable', terminals)
        page_config.setdefault('ignorePlugins', [])
        page_config.setdefault('serverRoot', server_root)
        page_config['store_id'] = self.application.store_id
        self.application.store_id += 1

        mathjax_config = self.settings.get('mathjax_config',
                                           'TeX-AMS_HTML-full,Safe')
        # TODO Remove CDN usage.
        mathjax_url = self.mathjax_url
        if not mathjax_url:
            mathjax_url = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js'

        page_config.setdefault('mathjaxConfig', mathjax_config)
        page_config.setdefault('fullMathjaxUrl', mathjax_url)

        # Add parameters parsed from the URL
        if mode == 'doc':
            page_config['mode'] = 'single-document'
        else:
            page_config['mode'] = 'multiple-document'
        page_config['workspace'] = workspace
        page_config['treePath'] = tree_path

        # Put all our config in page_config
        for name in config.trait_names():
            page_config[_camelCase(name)] = getattr(app, name)

        # Add full versions of all the urls
        for name in config.trait_names():
            if not name.endswith('_url'):
                continue
            full_name = _camelCase('full_' + name)
            full_url = getattr(app, name)
            if not is_url(full_url):
                # Relative URL will be prefixed with base_url
                full_url = ujoin(base_url, full_url)
            page_config[full_name] = full_url

        # Update the page config with the data from disk
        labextensions_path = app.extra_labextensions_path + app.labextensions_path
        recursive_update(page_config, get_page_config(labextensions_path, settings_dir, logger=self.log))

        # Write the template with the config.
        tpl = self.render_template('index.html', page_config=page_config)
        self.write(tpl)


class NotFoundHandler(LabHandler):
    def render_template(self, name, **ns):
        if 'page_config' in ns:
            ns['page_config'] = ns['page_config'].copy()
            ns['page_config']['notFoundUrl'] = self.request.path
        return super().render_template(name, **ns)


def add_handlers(handlers, extension_app):
    """Add the appropriate handlers to the web app.
    """
    # Normalize directories.
    for name in LabConfig.class_trait_names():
        if not name.endswith('_dir'):
            continue
        value = getattr(extension_app, name)
        setattr(extension_app, name, value.replace(os.sep, '/'))

    # Normalize urls
    # Local urls should have a leading slash but no trailing slash
    for name in LabConfig.class_trait_names():
        if not name.endswith('_url'):
            continue
        value = getattr(extension_app, name)
        if is_url(value):
            continue
        if not value.startswith('/'):
            value = '/' + value
        if value.endswith('/'):
            value = value[:-1]
        setattr(extension_app, name, value)

    url_pattern = MASTER_URL_PATTERN.format(extension_app.app_url.replace('/', ''))
    handlers.append((url_pattern, LabHandler))

    # Cache all or none of the files depending on the `cache_files` setting.
    no_cache_paths = [] if extension_app.cache_files else ['/']

    # Handle federated lab extensions.
    labextensions_path = extension_app.extra_labextensions_path + extension_app.labextensions_path
    labextensions_url = ujoin(extension_app.labextensions_url, "(.*)")
    handlers.append(
        (labextensions_url, FileFindHandler, {
            'path': labextensions_path,
            'no_cache_paths': no_cache_paths
        }))

    # Handle local settings.
    if extension_app.schemas_dir:
        settings_config = {
            'app_settings_dir': extension_app.app_settings_dir,
            'schemas_dir': extension_app.schemas_dir,
            'settings_dir': extension_app.user_settings_dir,
            'labextensions_path': labextensions_path
        }

        # Handle requests for the list of settings. Make slash optional.
        settings_path = ujoin(extension_app.settings_url, '?')
        handlers.append((settings_path, SettingsHandler, settings_config))

        # Handle requests for an individual set of settings.
        setting_path = ujoin(extension_app.settings_url, '(?P<schema_name>.+)')
        handlers.append((setting_path, SettingsHandler, settings_config))

    # Handle saved workspaces.
    if extension_app.workspaces_dir:

        workspaces_config = {
            'path': extension_app.workspaces_dir
        }

        # Handle requests for the list of workspaces. Make slash optional.
        workspaces_api_path = ujoin(extension_app.workspaces_api_url, '?')
        handlers.append((
            workspaces_api_path, WorkspacesHandler, workspaces_config))

        # Handle requests for an individually named workspace.
        workspace_api_path = ujoin(extension_app.workspaces_api_url, '(?P<space_name>.+)')
        handlers.append((
            workspace_api_path, WorkspacesHandler, workspaces_config))

    # Handle local listings.

    settings_config = extension_app.settings.get('config', {}).get('LabServerApp', {})
    blocked_extensions_uris = settings_config.get('blocked_extensions_uris', '')
    allowed_extensions_uris = settings_config.get('allowed_extensions_uris', '')

    if (blocked_extensions_uris) and (allowed_extensions_uris):
        print('Simultaneous blocked_extensions_uris and allowed_extensions_uris is not supported. Please define only one of those.')
        import sys
        sys.exit(-1)

    ListingsHandler.listings_refresh_seconds = settings_config.get('listings_refresh_seconds', 60 * 60)
    ListingsHandler.listings_request_opts = settings_config.get('listings_request_options', {})
    listings_url = ujoin(extension_app.listings_url)
    listings_path = ujoin(listings_url, '(.*)')

    if blocked_extensions_uris:
        ListingsHandler.blocked_extensions_uris = set(blocked_extensions_uris.split(','))
    if allowed_extensions_uris:
        ListingsHandler.allowed_extensions_uris = set(allowed_extensions_uris.split(','))

    fetch_listings(None)

    if len(ListingsHandler.blocked_extensions_uris) > 0 or len(ListingsHandler.allowed_extensions_uris) > 0:
        from tornado import ioloop
        ListingsHandler.pc = ioloop.PeriodicCallback(
            lambda: fetch_listings(None),
            callback_time=ListingsHandler.listings_refresh_seconds * 1000,
            jitter=0.1
            )
        ListingsHandler.pc.start()

    handlers.append((listings_path, ListingsHandler, {}))

    # Handle local themes.
    if extension_app.themes_dir:
        themes_url = extension_app.themes_url
        themes_path = ujoin(themes_url, '(.*)')
        handlers.append((
            themes_path,
            ThemesHandler,
            {
                'themes_url': themes_url,
                'path': extension_app.themes_dir,
                'labextensions_path': labextensions_path,
                'no_cache_paths': no_cache_paths
            }
        ))

    # Handle licenses.
    if extension_app.licenses_url:
        licenses_url = extension_app.licenses_url
        licenses_path = ujoin(licenses_url, '(.*)')
        handlers.append((
            licenses_path,
            LicensesHandler,
            {
                'manager': LicensesManager(parent=extension_app)
            }
        ))

    # Handle translations.
    if extension_app.translations_api_url:
        # Handle requests for the list of language packs available.
        # Make slash optional.
        translations_path = ujoin(extension_app.translations_api_url, '?')
        handlers.append((translations_path, TranslationsHandler, {'lab_config': extension_app}))

        # Handle requests for an individual language pack.
        translations_lang_path = ujoin(
            extension_app.translations_api_url, '(?P<locale>.*)')
        handlers.append((translations_lang_path, TranslationsHandler, {'lab_config': extension_app}))

    # Let the lab handler act as the fallthrough option instead of a 404.
    fallthrough_url = ujoin(extension_app.app_url, r'.*')
    handlers.append((fallthrough_url, NotFoundHandler))


def _camelCase(base):
    """Convert a string to camelCase.
    https://stackoverflow.com/a/20744956
    """
    output = ''.join(x for x in base.title() if x.isalpha())
    return output[0].lower() + output[1:]
