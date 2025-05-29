from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
class CustomerStock(models.Model):
    _name = 'customer.stock'
    _description = 'Customer Stock at Customer Location'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    sales_rep_id = fields.Many2one(related='customer_id.sales_rep_id', string="Sales Rep Name", store=True)
    quantity_on_hand = fields.Integer(string='Quantity On Hand', required=True)
    threshold = fields.Integer(string='Restock Threshold', required=True, default=0.0)
    last_updated = fields.Date(string='Last Updated', default=fields.Date.today)

    needs_restock = fields.Boolean(string='Needs Restock', compute='_compute_needs_restock', store=True)
    restock_rounds = fields.Integer(string='Restock Rounds', default=0)
    restock_status = fields.Char(
        string='Restock Status',
        compute='_compute_restock_status',
        store=True
    )
    restock_indicator = fields.Integer(
    string='Restock Status (Visual)',
    compute='_compute_restock_indicator',
    store=True
    )
    restock_status_for_color = fields.Selection(
    [
        ('yes', 'Needs Restocking'),
        ('no', 'Stock Okay'),

    ],
    string='Restock Status',
    compute='_compute_restock_status_for_color',
    store=True
    )
    #Compute restock status for color display 
    @api.depends('needs_restock')
    def _compute_restock_status_for_color(self):
        for rec in self:
            rec.restock_status_for_color = 'yes' if rec.needs_restock else 'no'
    
    # A salesperson can only see customers assigned to the same route they own
    # @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields=allfields, attributes=attributes)
        if self.user_has_groups('sales_route.group_salesperson'):
            res['customer_id']['domain'] = "[('route_id.sales_rep_id.user_id', '=', uid)]"
        return res
    # Constraint: Prevent duplicate product for same customer
    _sql_constraints = [
        ('unique_product_customer', 'unique(product_id, customer_id)', 'Each product can only have one stock record per customer.')
    ] 

    #Compute the restock status text label (used for visuals in kanban)
    @api.depends('needs_restock')
    def _compute_restock_status(self):
        for rec in self:
            rec.restock_status = "Needs Restock" if rec.needs_restock else "OK"

    # Compute numeric indicator (used for visuals in kanban)
    @api.depends('needs_restock')
    def _compute_restock_indicator(self):
        for rec in self:
            rec.restock_indicator = 1 if rec.needs_restock else 0
    
    #Compute if restock is needed based on threshold
    @api.depends('quantity_on_hand', 'threshold')
    def _compute_needs_restock(self):
        for record in self:
            if record.quantity_on_hand < record.threshold:
                if not record.needs_restock:
                    record.restock_rounds += 1
                record.needs_restock = True
            else:
                record.needs_restock = False

    #Manual method to reset restock counter
    def reset_restock_rounds(self):
        for record in self:
            record.restock_rounds = 0
