# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _

class CrmLead(models.Model):
    _inherit = "crm.lead"

    currency_id = fields.Many2one("res.currency", string="Valuta", required=True)

    val_equipements = fields.Monetary(compute="comu_val_equipement",currency_field="currency_id",store=True)
    val_equipement1 = fields.Monetary(currency_field="currency_id")
    val_equipement2 = fields.Monetary(currency_field="currency_id")
    val_equipement3= fields.Monetary(currency_field="currency_id")
    @api.depends('val_equipement1','val_equipement2','val_equipement3')
    def comu_val_equipement(self):
        for rec in self:
            rec.val_equipements = rec.val_equipement1 + rec.val_equipement2 + rec.val_equipement3



class SaleOrder(models.Model):
    _inherit = "sale.order"



    lieu_tournage = fields.Char(related="opportunity_id.x_studio_lieu_du_tournage")
    val_equipements = fields.Monetary(related="opportunity_id.val_equipements",store=True)




class AccountMoveInherit(models.Model):
    _inherit = "account.move"



    sale_order_id = fields.Many2one(
        comodel_name="sale.order",
        related="invoice_line_ids.sale_line_ids.order_id",
        string="Sales Order",
        ondelete="set null",
        store=True,
        index=True,
        copy=False,
    )

    origin = fields.Char(store=True, tracking=True,related="sale_order_id.origin")
    name_projet = fields.Char(store=True, tracking=True,related="sale_order_id.x_studio_nom_du_projet")
    lieu_tournage = fields.Char(store=True, tracking=True,related="sale_order_id.lieu_tournage")
    date_debut = fields.Date(store=True, tracking=True,related="sale_order_id.x_studio_date_de_cueillette")
    date_fin = fields.Date(store=True, tracking=True,related="sale_order_id.x_studio_date_de_retour")
    val_equipements = fields.Monetary(related="sale_order_id.val_equipements")
    date = fields.Date('Date', default=fields.Date.today)


    def action_task_send(self):
        self.ensure_one()
        template = self.env.ref("project_task_send_by_mail.email_task_template", False)
        compose_form = self.env.ref("mail.email_compose_message_wizard_form", False)
        ctx = dict(
            default_model="account.move",
            default_res_ids=self.ids,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode="comment",
        )
        return {
            "name": _("Compose Email"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form.id, "form")],
            "view_id": compose_form.id,
            "target": "new",
            "context": ctx,
        }

