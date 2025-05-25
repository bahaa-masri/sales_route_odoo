from odoo import models, fields, api
from datetime import date

class CustomerVisit(models.Model):
    _name = 'customer.visit'
    _description = 'Customer Visit'
    _sql_constraints = [
        ('unique_title', 'UNIQUE(name)', 'Visit Title must be unique.'),
    ]

    name = fields.Char(string='Visit Title', required=True,)
    route_id = fields.Many2one('sales.route', string='Sales Route', required=True)
    sales_rep_id = fields.Many2one(related='route_id.sales_rep_id', string='Sales Representative', store=True, readonly=True)
    route_day = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ], string='Visit Day', compute='_compute_route_day', store=True, readonly=True)

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


    total_sales_amount = fields.Float(string="Total Sales", compute="_compute_total_sales")
    products_need_restock_count = fields.Integer(
    string="Products Need Restock",
    related='customer_id.products_need_restock_count',
    store=True,
    readonly=True
)

#task fhmn , lself lval wklshi
    @api.model
    def create(self, vals):
        if 'check_in' in vals:
            if vals['check_in']:
                vals['visit_date'] = date.today()
            else:
                vals['visit_date'] = False
        return super().create(vals)
    
    def write(self, vals):
        if 'check_in' in vals:
            vals['visit_date'] = date.today() if vals['check_in'] else False
        return super().write(vals)

    # def write(self, vals):
    #     for rec in self:
    #         if 'check_in' in vals:
    #             if vals['check_in']:
    #                 vals['visit_date'] = date.today()
    #             else:
    #                 vals['visit_date'] = False
    #     return super().write(vals)
    

    # @api.onchange('route_id')
    # def _onchange_route_id(self):
    #     if self.customer_id:
    #         self.customer_id = False


    @api.depends('route_id')
    def _compute_route_day(self):
        if self.customer_id:
            self.customer_id = False
        if self.name:
            self.name = False
        for rec in self:
            rec.route_day = rec.route_id.visit_days or ''

    @api.onchange('customer_id')
    def _onchange_route_id(self):
        if self.customer_id:
            if self.route_id:
                customer_id = self.customer_id.name or 'Rcustomerep'
                route_name = self.route_id.name or 'Route'
                today = fields.Date.today().strftime('%Y-%m-%d')
                self.name = f"{route_name} - {customer_id} - {today}"

    @api.onchange('check_in')
    def _onchange_check_in(self):
        for rec in self:
            if rec.check_in:
                rec.visit_date = fields.Date.today()
            else:
                rec.visit_date = False

##11111111111111111111111S
    #@api.depends('sale_order_ids.amount_total')
    def _compute_total_sales(self):
        for partner in self:
            #total = sum(order.amount_total for order in partner.sale_order_ids if order.state in ['sale', 'done'])
            total=0
            partner.total_sales_amount = total
