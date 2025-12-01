from odoo import models, fields, api

class TaggProcessOpportunity(models.Model):
    _name = 'tagg.process.opportunity'
    _description = 'TAGG Process Opportunity'
    _order = 'entry_date desc, id desc'
    
    process_id = fields.Many2one('tagg.process', string='Process', required=True, ondelete='cascade')
    entry_date = fields.Date(string='Entry Date', required=True, default=fields.Date.today)
    identified_opportunity = fields.Text(string='Identified Opportunity', required=True)
    means_to_take_advantage = fields.Text(string='Means to Take Advantage')
    deadline = fields.Date(string='Deadline')
    
    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)