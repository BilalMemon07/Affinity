{
    'name': "Scheme",
    'version': '16.0',
    'depends': ['base','sale'],
    'author': "Muhammad Faraz",
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