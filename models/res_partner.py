from odoo import models, fields, api
from datetime import date, timedelta

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_stock_ids = fields.One2many(
        'customer.stock', 'customer_id', string="Customer Stock"
    )
    products_need_restock_count = fields.Integer(
        string="Products Need Restock",
        compute="_compute_products_need_restock_count",
        store=True
    )
    region_id = fields.Many2one('region', string='region ')
    route_id = fields.Many2one('sales.route', string='Assigned Route', compute="_compute_route", store=True)
    visit_not_done_recently = fields.Boolean(string="Visited in Last Week", compute="_compute_visit_not_done_recently", store=True)
    customer_visit_ids = fields.One2many('customer.visit', 'customer_id', string="Visits")
    sales_rep_id = fields.Many2one('sales.representative', related='route_id.sales_rep_id', store=True) 
    @api.depends('region_id')
    def _compute_route(self):
        for partner in self:
            if partner.region_id:
                route = self.env['sales.route'].search([
                    ('region_ids', 'in', [partner.region_id.id])
                ], limit=1)
                partner.route_id = route
            else:
                partner.route_id = False

    @api.depends('customer_visit_ids.visit_date')
    def _compute_visit_not_done_recently(self):
        for partner in self:
            recent_visits = partner.customer_visit_ids.filtered(
                lambda v: v.visit_date and v.visit_date >= date.today() - timedelta(days=7)
            )
            partner.visit_not_done_recently = bool(recent_visits)
    @api.depends('customer_stock_ids.needs_restock')
    def _compute_products_need_restock_count(self):
        for partner in self:
            partner.products_need_restock_count = len([
                stock for stock in partner.customer_stock_ids
                if stock.needs_restock
            ])