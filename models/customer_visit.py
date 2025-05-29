from odoo import models, fields, api
from datetime import date

# Model for customer visit records
class CustomerVisit(models.Model):
    _name = 'customer.visit'
    _description = 'Customer Visit'

    name = fields.Char(string='Visit Title', required=True,)
    route_id = fields.Many2one('sales.route', string='Sales Route', required=True)
    sales_rep_id = fields.Many2one(related='route_id.sales_rep_id', string='Sales Representative', store=True, readonly=True)
    route_day = fields.Selection(
        related='route_id.visit_days',
        string='Visit Day',
        store=True,
        readonly=True
    )
    customer_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        domain="[('route_id', '=', route_id)]"
    )
    visit_date = fields.Date(string='Visit Date', store=True , readonly=True)
    objective = fields.Text(string='Visit Objective')
    check_in = fields.Boolean(string='Checked In')
    customer_feedback = fields.Text(string="Customer Feedback")
    sales_discussions = fields.Text(string="Sales Discussions")
    visit_outcome = fields.Text(string="Visit Outcome / Notes")
    products_need_restock_count = fields.Integer(
        string="Products Need Restock",
        related='customer_id.products_need_restock_count',
        store=True,
        readonly=True
    )

    # Unique constraint on visit title
    _sql_constraints = [
        ('unique_title', 'UNIQUE(name)', 'Visit Title must be unique.'),
    ]

# Clear customer and visit title when route changes
    @api.onchange('route_id')
    def _route_day(self):
        if self.customer_id:
            self.customer_id = False
        if self.name:
            self.name = False

# Auto-generate visit title when customer selected
    @api.onchange('customer_id')
    def _onchange_route_id(self):
        if self.customer_id:
            if self.route_id:
                customer_id = self.customer_id.name or 'Rcustomerep'
                route_name = self.route_id.name or 'Route'
                today = fields.Date.today().strftime('%Y-%m-%d')
                self.name = f"{route_name} - {customer_id} - {today}"

    # Update visit date when check-in status changes
    @api.onchange('check_in')
    def _onchange_check_in(self):
        for rec in self:
            if rec.check_in:
                rec.visit_date = fields.Date.today()
            else:
                rec.visit_date = False

    # Set visit date if checked in during creation
    @api.model
    def create(self, vals):
        if 'check_in' in vals:
            if vals['check_in']:
                vals['visit_date'] = date.today()
            else:
                vals['visit_date'] = False
        return super().create(vals)
    
    # Update visit date on check-in change during edit
    def write(self, vals):
        if 'check_in' in vals:
            vals['visit_date'] = date.today() if vals['check_in'] else False
        return super().write(vals)
