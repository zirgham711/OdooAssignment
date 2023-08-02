{

  'name': "Invoice Management",

  'version': '1.0',

  'depends': ['base','estate'],

  'author': "Zirgham Hassan",

  'category': 'Category',

  'description': """

  This is a test module of Invoice Management!

  Written for the Odoo Quickstart Tutorial.

  """,

  # data files always loaded at installation

  'data': [
'security/ir.model.access.csv',
'views/property_invoice_view.xml'
  ],

  'installable': True,

  'auto_install': False,

  'application': False,

}