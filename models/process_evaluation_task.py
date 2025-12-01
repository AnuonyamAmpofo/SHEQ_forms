from odoo import models, fields, api

class ProcessEvaluationTask(models.Model):
    _name = 'process.evaluation.task'
    _description = 'Process Evaluation Task'
    _order = 'sequence, id'
    
    # Link to main evaluation
    process_evaluation_id = fields.Many2one(
        'tagg.process.evaluation',
        string='Process Evaluation',
        required=True,
        ondelete='cascade'
    )
    
    sequence = fields.Integer(string='Sequence', default=10)
    title = fields.Char(string='TITLE', required=True)
    memo = fields.Char(string='MEMO')
    date = fields.Date(string='DATE')
    time = fields.Float(string='TIME')
    type = fields.Char(string='TYPE')
    direction = fields.Char(string='DIRECTION')