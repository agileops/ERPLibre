# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'MathBenTech Enterprise Services for utility business',
    'version': '0.1',
    'author': "MathBenTech",
    'website': 'https://mathben.tech',
    'license': 'AGPL-3',
    'category': 'Other',
    'summary': 'Services for utility business',
    'description': """
MathBenTech Enterprise Services for utility business
====================================================
All modules needed for enterprise with services for utility business.
""",
    'depends': [
        # MathBenTech
        'mathbentech_base_enterprise',

        # Custom MathBenTech
        'product_lump_sum',
        # 'sale_margin_percent',
        'sale_report_margin',
        'sale_order_margin_percent',
        'sale_margin_security',
        'sale_product_manufacturer',
        'sale_product_manufacturer_model',
        # 'sale_hide_tax_sale_order_lines', # Bug
        'sale_crm_auto_update_lead',
        'crm_marge',
        'menu_force_project_first',
        'crm_working_date',
        'helpdesk_service_call',
        'website_helpdesk',
        'website_portal_contact',
        'website_portal_address',

        # OCA sale-workflow
        'sale_order_revision',
        'sale_double_validation',

        # OCA helpdesk
        'helpdesk_mgmt',

        # General
        'digest',  # KPI
    ],
    'data': [],
    'installable': True,
}
