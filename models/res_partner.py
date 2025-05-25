from odoo import models, fields, api
from datetime import date, timedelta

class ResPartner(models.Model):
    _inherit = 'res.partner'

    total_sales_amount = fields.Float(string="Total Sales", compute="_compute_total_sales")
    customer_stock_ids = fields.One2many(
        'customer.stock', 'customer_id', string="Customer Stock"
    )
    products_need_restock_count = fields.Integer(
        string="Products Need Restock",
        compute="_compute_products_need_restock_count",
        store=True
    )
    REGION_SELECTION = [
    ('north', 'North'),
    ('south', 'South'),
    ('east', 'East'),
    ('west', 'West'),
]

    city = fields.Selection(REGION_SELECTION, string='City')

    route_id = fields.Many2one('sales.route', string='Assigned Route', compute="_compute_route", store=True)
    visit_done_recently = fields.Boolean(string="Visited in Last Week", compute="_compute_visit_done_recently", store=True)
    customer_visit_ids = fields.One2many('customer.visit', 'customer_id', string="Visits")
    sales_rep_id = fields.Many2one('sales.representative', related='route_id.sales_rep_id', store=True) 
    route_name = fields.Char(string="Route Name", compute="_compute_route_name", store=True)
    @api.depends('route_id.name')
    def _compute_route_name(self):
        for rec in self:
            rec.route_name = rec.route_id.name if rec.route_id else False
    @api.depends('city')
    def _compute_route(self):
        for partner in self:
            route = self.env['sales.route'].search([('region', '=', partner.city)], limit=1)
            partner.route_id = route if route else False
#mesh mni7a
    # @api.depends('customer_visit_ids.visit_date')
    # def _compute_visit_done_recently(self):
    #     for partner in self:
    #         recent_visit = self.env['customer.visit'].search([
    #             ('customer_id', '=', partner.id),
    #             ('visit_date', '>=', date.today() - timedelta(days=7))
    #         ], limit=1)
    #         partner.visit_done_recently = bool(recent_visit)

    
    @api.depends('customer_visit_ids.visit_date')
    def _compute_visit_done_recently(self):
        for partner in self:
            recent_visits = partner.customer_visit_ids.filtered(
                lambda v: v.visit_date and v.visit_date >= date.today() - timedelta(days=7)
            )
            partner.visit_done_recently = bool(recent_visits)

    @api.depends('customer_stock_ids.needs_restock')
    def _compute_products_need_restock_count(self):
        for partner in self:
            partner.products_need_restock_count = len([
                stock for stock in partner.customer_stock_ids
                if stock.needs_restock
            ])
    @api.depends('sale_order_ids.amount_total')
    def _compute_total_sales(self):
        for partner in self:
            total = sum(order.amount_total for order in partner.sale_order_ids if order.state in ['sale', 'done'])
            partner.total_sales_amount = total
