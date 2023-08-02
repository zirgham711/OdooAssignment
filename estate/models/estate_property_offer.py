from odoo import api, fields, models
from datetime import datetime, timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string="Status", no_copy=True, default='refused')
    buyer_id = fields.Many2one("res.partner", string="Partner", required=True, domain=[('is_company', '=', False)])
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (Days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.date_deadline = False
            else:
                create_date = fields.Datetime.from_string(record.create_date)
                record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                create_date = fields.Datetime.from_string(record.create_date)
                deadline_date = fields.Datetime.from_string(record.date_deadline)
                record.validity = (deadline_date - create_date).days
            else:
                record.validity = 7

    @api.onchange('validity', 'create_date')
    def _onchange_validity(self):
        if self.validity and self.create_date:
            create_date = fields.Datetime.from_string(self.create_date)
            self.date_deadline = create_date + timedelta(days=self.validity)

    def write(self, vals):
        if 'status' in vals and vals['status'] == 'accepted':
            accepted_offers_before_write = self.filtered(lambda offer: offer.status == 'accepted')

            for offer in self:

                other_offers = offer.property_id.offer_ids - offer
                other_offers.write({'status': 'refused'})
                offer.property_id.write({'selling_price': offer.price})

            accepted_offers_after_write = self.filtered(lambda offer: offer.status == 'accepted')

            if len(accepted_offers_before_write) != len(accepted_offers_after_write):
                raise ValidationError("Only one offer can be accepted.")

        return super(EstatePropertyOffer, self).write(vals)

    def accept_offer(self):
        for offer in self:
            if offer.status != 'accepted':
                offer.status = 'accepted'
                offer.property_id.buyer_id = offer.buyer_id

    def refuse_offer(self):
        for offer in self:
            if offer.status != 'refused':
                offer.status = 'refused'

    _sql_constraints = [
        ('price', 'CHECK(price > 0)',
         'Offer Price must be strictly positive!')
    ]
