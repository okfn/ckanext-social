Social Extension
================

The Social extension allows site visitors to share pages on social
networking sites.

NOTE: This extension requires ckan version 1.7 or higher.

Activating and Installing
-------------------------

To install the plugin, enter your virtualenv and load the source::

 (pyenv)$ git install -e hg+https://github.com/okfn/ckanext-social#egg=ckanext-social

Add the following to your CKAN .ini file::

 ckan.plugins = social <other-plugins>

Using the Extension
-------------------

ShareThis
~~~~~~~~~

To enable sharing via the ShareThis service you must first get an API
Key from ShareThis.com and the add it to your CKAN .ini file::

 social.sharethis_api_key = <Your ShareThis.com API Key>

Other options can also be set here::

 social.sharethis_style = horizontal | vertical | large | none
 social.sharethis_sites = googleplus twitter facebook sharethis email
 social.sharethis_multipost = true | false

Sharing can now be added using the social_sharethis() function inside a
template::

 ${h.social_sharethis()}

Templates can overide the config options if desired::

 ${h.social_sharethis(style='large', sites=['twitter', 'facebook'])}

