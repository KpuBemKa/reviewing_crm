from odoo import models, fields


class ReviewingTag(models.Model):
    _name = "rvg.tags"
    _description = "Tags for reviewing CRM tasks"

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer(string="Color")
