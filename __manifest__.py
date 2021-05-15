# -*- coding: utf-8 -*-
{
    'name': "Hospital Agustín",

    'summary': """
    """,

    'description': """
    """,

    'author': "Agustín Galera",
    'website': "",
    'license': '',
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
    ],

    # always loaded
    'data': [
        'views/informes_views.xml',
        'views/menus.xml',
        'views/tratamiento_views.xml',
        'views/paciente_views.xml',
        'reports/report_hospital.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
