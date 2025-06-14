{
    'name': 'Sales Route Planning',
    'version': '2.0',
    'summary': 'Manage sales routes and visits for Global Distributors',
    'description': """
        Internship project developed by Bahaa Masri for NavyBits.
        Sales Route Planning and Monitoring System for the fictional company Global Distributors.
    """,
    'author': 'bahaa',
    'category': 'Sales',
    'depends': ['base','sale_management'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/sales_dashboard_views.xml',
        'views/menu.xml',
         'views/customer_stock_views.xml',
        'views/actions.xml',
        'views/sales_route_views.xml',
        'views/customer_visit_views.xml',
        'views/res_partner_views.xml',
        'views/region_views.xml',
        'views/sales_representative.xml',
    ],
    'installable': True,
    "application": True,
}
