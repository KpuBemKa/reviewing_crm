from odoo import models, fields


class ReviewingTag(models.Model):
    _name = "rvg.tags"
    _description = "Tags for reviewing CRM tasks"

    color = fields.Integer(string="Color")
    name = fields.Char(string="Tag Name", required=True)
