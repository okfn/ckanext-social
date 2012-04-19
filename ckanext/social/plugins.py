import ckan.plugins as p

available_sites = {'sharethis' : 'ShareThis',
                   'twitter' : 'Tweet',
                   'facebook' : 'Facebook',
                   'googleplus' : 'Google +1',
                   'email' : 'Email',}

styles = {'horizontal' : '_hcount',
          'vertical' : '_vcount',
          'none' : '',
          'large' : '_large'}


class Social(p.SingletonPlugin):

    p.implements(p.IConfigurer)
    p.implements(p.IConfigurable)
    p.implements(p.ITemplateHelpers)

    def configure(self, config):
        style = config.get('social.sharethis_style', 'horizontal')
        style = styles.get(style, '')

        sites = config.get('social.sharethis_sites','sharethis')
        sites = p.toolkit.aslist(sites)

        multipost = config.get('social.sharethis_multipost', 'true')
        multipost = p.toolkit.asbool(multipost)

        # store these so available to class methods
        self.__class__.style = style
        self.__class__.sites = sites
        self.__class__.multipost = multipost

    def update_config(self, config):
        # add template directory
        p.toolkit.add_template_directory(config, 'templates')

    @classmethod
    def sharethis(cls, style=None, sites=None, multipost=None):
        ''' create share this buttons and add them to the template '''
        # override default style
        if style:
            style = styles[style]
        else:
            style = cls.style

        # override default sites
        if not sites:
            sites = cls.sites

        # override default multipost
        if multipost is None:
            multipost = cls.multipost

        links = []
        for site in cls.sites:
            if site in available_sites:
                data = (site, style, available_sites[site])
                links.append('<span class="st_%s%s" displayText="%s"></span>' % data)

        buttons = p.toolkit.literal('\n'.join(links))
        data = {'buttons' : buttons, 'switchTo5x' : multipost}
        return p.toolkit.render_snippet('sharethis.html', data)

    def get_helpers(self):
        return {'social_sharethis': self.sharethis}
