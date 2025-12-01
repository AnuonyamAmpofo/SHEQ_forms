from odoo import models, fields, api

class TaggProcessLegalRequirement(models.Model):
    _name = 'tagg.process.legal.requirement'
    _description = 'TAGG Process Legal Requirement'
    
    process_id = fields.Many2one('tagg.process', string='Process', required=True, ondelete='cascade')
    legal_requirement = fields.Char(string='Legal Requirement associated with the Process', required=True)
    specific_law_or_regulation = fields.Char(string='Specific Law or Regulation')
    institution = fields.Char(string='Institution')
    
    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)