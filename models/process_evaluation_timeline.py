from odoo import models, fields, api

class ProcessEvaluationTimeline(models.Model):
    _name = 'process.evaluation.timeline'
    _description = 'Process Evaluation Timeline'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)
    process_evaluation_id = fields.Many2one('tagg.process.evaluation', string='Process Evaluation')
    time = fields.Char(string='Time')
    memo = fields.Char(string='Memo')
    date = fields.Date(string='Date')


    # <header>
                        # <button name="action_complete" type="object" string="Save" class="btn-primary"/>
                    #     <button name="action_cancel" type="object" string="Cancel" class="btn-secondary"/>
                    # </header>
    # 