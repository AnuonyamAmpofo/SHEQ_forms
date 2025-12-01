from odoo import models, fields, api


class TaggProcessQMSRisk(models.Model):
    _name = 'tagg.process.qms.risk'
    _description = 'TAGG Process QMS Risk'
    _order = 'year desc, id desc'
    
    process_id = fields.Many2one('tagg.process', string='Process', required=True, ondelete='cascade')
    year = fields.Integer(string='Year', required=True)
    risk_description = fields.Text(string='Risk Description', required=True)
    likelihood_of_risk = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Likelihood of Risk Occurring')
    severity_of_impact = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Severity of Impact')
    risk = fields.Text(string='Risk')
    risk_priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Risk Priority')
    existing_controls = fields.Text(string='Existing Controls')
    further_controls_required = fields.Text(string='Further Controls Required')
    resources_for_controls = fields.Text(string='Resources Required')
    owner = fields.Char(string='Owner')
    timescale_for_actions = fields.Char(string='Timescale for Actions')
    
    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)