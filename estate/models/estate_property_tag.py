from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(string="Name", required=True)

    _sql_constraints = [
        ('unique_property_tag_name', 'unique(name)', 'Property Tag name must be unique!')
    ]
