# -*- coding: utf-8 -*-

{
  'name' : 'Set Home Action',
  'summary' : 'Set Home Action',
  'category' : 'Extra Tools',
  'version' : '10.0.1.0.1',
  'description' : 'Set Home Action',
  'website': 'https://pandoratech.ae',
  'author': 'Pandora Tech LLC',
  'price': 5.00, 
  'currency': 'EUR',
  'depends' : ['web'],
  'data' : ['views/assets.xml'],
  'qweb' : ['static/src/xml/set_home_action.xml'],
  'images': ['static/description/banner.jpg'],
  'application' : True,
  'installable' : True,
  'auto_install' : False,
  'pre_init_hook' : "pre_init_check",
  'license': 'OPL-1',
}
