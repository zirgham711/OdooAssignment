{

  'name': "Real-Estate Management",

  'version': '1.0',

  'depends': ['base'],

  'author': "Zirgham Hassan",

  'category': 'Category',

  'description': """

  This is a test module of Real-Estate Management!

  Written for the Odoo Quickstart Tutorial.

  """,

  'data': [

'security/ir.model.access.csv',
    'views/property_views.xml',
    'views/estate_property_type_views.xml',
    'views/estate_property_offers_views.xml',
     'views/res_users_inheritViews.xml',
  ],

  'installable': True,

  'auto_install': False,

  'application': False,

}