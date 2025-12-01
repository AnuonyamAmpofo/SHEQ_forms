from odoo import models, fields, api

class TaggProcessEvaluation(models.Model):
    _name = 'tagg.process.evaluation'
    _description = 'TAGG Process Evaluation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='ID', required=True, default='New')
    
    # QMS PROCESS section
    qms_process = fields.Selection([
        ('document_control', 'Document Control'),
        ('internal_audit', 'Internal Audit'),
        ('corrective_action', 'Corrective Action'),
        ('management_review', 'Management Review'),
        ('risk_assessment', 'Risk Assessment'),
        ('training_competence', 'Training & Competence'),
        ('calibration', 'Calibration'),
        ('supplier_management', 'Supplier Management'),
        ('customer_feedback', 'Customer Feedback'),
        ('incident_investigation', 'Incident Investigation'),
        ('other', 'Other'),
    ], string='QMS PROCESS', required=True)
    
    number_of_ncs = fields.Integer(string='NUMBER OF NCS', default=0)
    process_score = fields.Integer(string='PROCESS SCORE', default=5)
    comments = fields.Text(string='COMMENTS')
    
    # Task entries section - One2many to the separate task model
    task_ids = fields.One2many(
        'process.evaluation.task',
        'process_evaluation_id',
        string='Tasks'
    )
    
    # PROCESS OWNER section
    process_owner_id = fields.Many2one(
        'res.users',
        string='PROCESS OWNER',
        default=lambda self: self.env.user,
        required=True
    )
    evaluation_date = fields.Date(string='EVALUATION DATE', default=fields.Date.today)
    period_of_assessment_from = fields.Date(string='PERIOD OF ASSESSMENT FROM')
    period_of_assessment_to = fields.Date(string='TO')
    
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', 'New') == 'New':
            last_record = self.search([], order='id desc', limit=1)
            if last_record and last_record.name.isdigit():
                next_number = int(last_record.name) + 1
            else:
                next_number = 1
            vals_list['name'] = str(next_number)
        return super().create(vals_list)
    
    def action_complete(self):
        self.write({'status': 'completed'})
        return True
    
    def action_cancel(self):
        self.write({'status': 'cancelled'})
        return True
    
    def action_draft(self):
        self.write({'status': 'draft'})
        return True
    
    def action_remove_all_main_data(self):
        self.write({
            'qms_process': False,
            'number_of_ncs': 0,
            'process_score': 5,
            'comments': False,
        })
        return True