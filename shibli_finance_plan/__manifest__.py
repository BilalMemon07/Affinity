{
    'name': "Finance Plan",
    'version': '16.0',
    'depends': ['base','uom','product','account'],
    'author': "Muhammad Bilal",
    'category': 'Category',
    'images' : ['static/description/icon.png'],
    'website': "https://www.affinitysuite.net",
    'description': """
    Description text
    """,
    'application': True,
    # data files always loaded at installation
    'data': [
        'views/view.xml',
        'security/ir.model.access.csv',
    ],
}