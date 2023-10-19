{
    'name': "Shipment Plan",
    'version': '16.0',
    'depends': ['base','stock'],
    'author': "Muhammad Bilal",
    'category': 'Category',
    'images' : ['static/description/icon.png'],
    'description': """
    Description text
    """,
    'application': True,
    # data files always loaded at installation
    'data': [
        'views/views.xml',
        'security/ir.model.access.csv',
    ],
}