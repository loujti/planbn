from odoo import _, api, fields, models
from datetime import date, datetime


class ResParternerinherit(models.Model):
    _inherit = "res.partner"

    lead_id = fields.Many2one('crm.lead')
    # move_partner_id = fields.Many2one('account.move',string='Service')

    # x_studio_lieu_du_tournage = fields.Char(related='lead_id.x_studio_lieu_du_tournage')
    create_date = fields.Datetime(related='lead_id.create_date')
    # invoice_date = fields.Date(related='move_partner_id.invoice_date')






