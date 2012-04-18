import os
from webhelpers.html.tags import literal

import ckan.plugins as plugins
import ckan.lib.base as base
import ckanext.social

available_sites = {'sharethis' : 'ShareThis',
                   'twitter' : 'Tweet',
                   'facebook' : 'Facebook',
                   'googleplus' : 'Google +1',
                   'email' : 'Email',}

styles = {'horizontal' : '_hcount',
          'vertical' : '_vcount',
          'none' : '',
          'large' : '_large'}

def configure_template_directory(config, relative_path):
    configure_served_directory(config, relative_path, 'extra_template_paths')

def configure_public_directory(config, relative_path):
    configure_served_directory(config, relative_path, 'extra_public_paths')

def configure_served_directory(config, relative_path, config_var):
    'Configure serving of public/template directories.'
    assert config_var in ('extra_template_paths', 'extra_public_paths')
    this_dir = os.path.dirname(ckanext.social.__file__)
    absolute_path = os.path.join(this_dir, relative_path)
    if absolute_path not in config.get(config_var, ''):
        if config.get(config_var):
            config[config_var] += ',' + absolute_path
        else:
            config[config_var] = absolute_path


class Social(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.ITemplateHelpers)

    def configure(self, config):
        self.__class__.config = config
        self.__class__.sites = config.get('social.sharethis_sites','sharethis').split()
        style = config.get('social.sharethis_style', 'horizontal')
        self.__class__.style = styles[style]

    def update_config(self, config):
        configure_template_directory(config, 'templates')
        #configure_public_directory(config, 'public')

    @classmethod
    def sharethis(cls, style=None, sites=None):
        ''' create share this buttons and add them to the template '''
        # override default style
        if style:
            style = styles[style]
        else:
            style = cls.style

        # override default sites
        if not sites:
            sites = cls.sites

        links = []
        for site in cls.sites:
            if site in available_sites:
                data = (site, style, available_sites[site])
                links.append('<span class="st_%s%s" displayText="%s"></span>' % data)

        buttons = literal('\n'.join(links))
        return literal(base.render('sharethis.html', {'buttons' : buttons}))

    def get_helpers(self):
        return {'social_sharethis': self.sharethis}
