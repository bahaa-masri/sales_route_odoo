from odoo import models, fields, api
from odoo.exceptions import ValidationError
class SalesRepresentative(models.Model):
    _name = 'sales.representative'
    _description = 'Sales Representative'

    name = fields.Char(string='Name', required=True)
    user_id = fields.Many2one('res.users', string='Related User')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')

class Region(models.Model):
    _name = 'region'
    _description = 'Region'

    name = fields.Char(string='Region', required=True)

class SalesRoute(models.Model):
    _name = 'sales.route'
    _description = 'Sales Route'

    name = fields.Char(string='Route Name', required=True)
    region_ids = fields.Many2many('region', string='Regions')
    sales_rep_id = fields.Many2one('sales.representative', string='Sales Representative', required=True)
    visit_days = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ], string='Visit Day')

    @api.constrains('region_ids', 'visit_days', 'sales_rep_id')
    def _check_route_overlap(self):
        for record in self:
            overlap = self.search([
                ('id', '!=', record.id),
                ('region_ids', 'in', record.region_ids.ids),
                ('visit_days', '=', record.visit_days),
                ('sales_rep_id', '=', record.sales_rep_id.id)
            ])
            if overlap:
                raise ValidationError(
                    "This sales representative already has a route in this region on this day!") 
              
    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            existing = self.search([
                ('id', '!=', record.id),
                ('name', '=', record.name)
            ])
            if existing:
                raise ValidationError("Route name must be unique!")
