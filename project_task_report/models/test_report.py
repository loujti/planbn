
from odoo import models, api, _



class CrmStatisticsReport(models.AbstractModel):
    _name = 'report.project_task_report.task_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        employees = self.env['sale.order'].search([])


        return {
            'docs': docids,
            'data': data,
            'employees': employees,
            'self': self
                }
