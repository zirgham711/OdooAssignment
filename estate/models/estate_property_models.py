from odoo import api, fields, models
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError


class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Model for Real-Estate Properties"

    name = fields.Char(string="Title", required=True, default="Unknown")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Post Code")
    date_availability = fields.Date(string="Availability From", default=datetime.now() + timedelta(days=90))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer(string="Bedrooms", default=3)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
            ('northeast', 'Northeast'),
            ('northwest', 'Northwest'),
            ('southeast', 'Southeast'),
            ('southwest', 'Southwest'),
        ],
        string="Garden Orientation",
    )
    last_seen = fields.Datetime(string="Last Seen", default=lambda self: fields.Datetime.now())
    property_type_id = fields.Many2one("estate.property.type", string="Property Type", options="{'no_create': True, 'no_create_edit': True}")
    buyer_id = fields.Many2one("res.partner", string="Buyer", domain="[('is_company', '=', False)]", no_copy=True)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", domain="[('user_ids', '!=', False)]", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)", store=True)
    best_offer = fields.Float(compute="_compute_highest_offer", string="Highest Offer", store=True)

    status = fields.Selection([
        ('new', 'New'),
        ('canceled', 'Canceled'),
        ('sold', 'Sold'),
    ], string="Status", default='new', readonly=True, copy=False)

    def cancel(self):
        for record in self:
            if record.status == 'sold':
                raise UserError("A sold property cannot be canceled.")
            if record.status != 'canceled':
                record.status = 'canceled'

    def sold(self):
        for record in self:
            if record.status == 'canceled':
                raise UserError("A canceled property cannot be sold.")
            if record.status != 'sold':
                record.status = 'sold'
                record.generate_invoice()

    _sql_constraints = [
        ('check_positive_prices', 'CHECK(expected_price > 0 AND selling_price > 0)', 'Expected Price and Selling Price must be strictly positive!')
    ]

    def generate_invoice(self):
        self.ensure_one()
        if self.status == 'sold' and self.buyer_id:
            invoice_data = {
                'buyer_id': self.buyer_id.id,
                'property_id': self.id,
                'amount': self.selling_price,
            }
            self.env['estate.property.invoice'].create(invoice_data)

    @api.model
    def create(self, vals):

        if 'selling_price' not in vals:
            vals['selling_price'] = 0.0
        return super(EstateProperties, self).create(vals)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_highest_offer(self):
        for property in self:
            highest_offer = max(property.offer_ids.mapped("price"), default=0.0)
            property.best_offer = highest_offer

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:

            self.garden_area = 10
            self.garden_orientation = 'north'
        else:

            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for property in self:
            # Skip the constraint check if expected_price is not set (i.e., it is zero)
            if not property.expected_price:
                continue

            if property.selling_price and (property.selling_price < 0.9 * property.expected_price or property.selling_price < 0):
                raise ValidationError("Selling price cannot be lower than 90% of the expected price or negative!")

            if property.status == 'new' and any(offer.status == 'accepted' for offer in property.offer_ids):
                raise ValidationError("Selling price cannot be set until an offer is validated!")

    @api.constrains('selling_price')
    def _check_selling_price_with_offer(self):
        for property in self:
            if property.status == 'new' and any(offer.status == 'accepted' for offer in property.offer_ids):
                raise ValidationError("Selling price cannot be set until an offer is validated!")

