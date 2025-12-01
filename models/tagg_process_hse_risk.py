from odoo import models, fields, api

class TaggProcessHSERisk(models.Model):
    _name = 'tagg.process.hse.risk'
    _description = 'TAGG Process HSE Risk'
    _order = 'year desc, id desc'
    
    process_id = fields.Many2one('tagg.process', string='Process', required=True, ondelete='cascade')
    year = fields.Integer(string='Year', required=True)
    process_performance_location = fields.Char(string='Process Performance Location')
    activity = fields.Char(string='Activity', required=True)
    risk_description = fields.Text(string='Risk Description and Possible Effects', required=True)
    affected_parties = fields.Text(string='Who Might be Harmed/What could be damaged and how>?)', required=True)
    likelihood_of_risk = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Likelihood of Risk Occurring')
    risk = fields.Text(string='Risk')
    risk_priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Risk Priority')
    severity_of_impact = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Severity of Impact if the Risk Occurs')
    # expected_impact = fields.Text(string='Expected Impact')

    
    risk_rating = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Risk Rating')


    existing_controls = fields.Text(string='What is already being done')
    further_controls_required = fields.Text(string='What further controls are required')
    resources_for_controls = fields.Text(string='Resources Required')
    risk_management_approach = fields.Text(string='Risk Management Approach')
    timescale_for_actions = fields.Char(string='Timescale for Actions')
    
    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)