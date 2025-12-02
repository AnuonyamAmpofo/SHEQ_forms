from odoo import models, fields, api
from datetime import date

class StakeholdersEngagementPlan(models.Model):
    _name = 'stakeholders.engagement.plan'
    _description = 'Stakeholder Engagement Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    # Form Header Fields
    name = fields.Char(
        string='Reference',
        default=lambda self: self.env['ir.sequence'].next_by_code('stakeholders.engagement.plan'),
        readonly=True
    )
    
    # Year as Selection field (dropdown)
    year = fields.Selection(
        string='YEAR *',
        selection='_get_year_selection',
        required=True
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft', tracking=True)
    
    # Plan Section - One2many for lines
    engagement_line_ids = fields.One2many(
        'stakeholder.engagement.line',
        'engagement_id',
        string='Engagement Activities'
    )
    
    # Method to generate year selection
    @api.model
    def _get_year_selection(self):
        """Generate year selection from current year - 5 to current year + 5"""
        current_year = date.today().year
        years = []
        for year in range(current_year - 5, current_year + 6):
            years.append((str(year), str(year)))
        return years
    
    # Default year to current year
    @api.model
    def default_get(self, fields_list):
        res = super(StakeholdersEngagementPlan, self).default_get(fields_list)
        current_year = date.today().year
        res['year'] = str(current_year)
        return res
    
    # Button actions
    def action_save(self):
        return {'type': 'ir.actions.act_window_close'}
    
    def action_submit(self):
        self.write({'state': 'submitted'})
    
    def action_cancel(self):
        self.write({'state': 'draft'})
    
    def action_approve(self):
        self.write({'state': 'approved'})
    
    def action_reject(self):
        self.write({'state': 'rejected'})
    
    @api.model_create_multi
    def create(self, vals_list):
        """Override create method to handle batch creation"""
        return super(StakeholdersEngagementPlan, self).create(vals_list)


class StakeholderEngagementLine(models.Model):
    _name = 'stakeholder.engagement.line'
    _description = 'Stakeholder Engagement Line'
    _order = 'date asc'
    
    engagement_id = fields.Many2one(
        'stakeholders.engagement.plan',
        string='Engagement Plan',
        ondelete='cascade',
        required=True
    )
    
    # Fields from your form
    stakeholder_group = fields.Char(string='STAKEHOLDER GROUP *', required=True)
    method_of_exploration = fields.Char(string='METHOD OF EXPLORATION *', required=True)
    date = fields.Date(string='DATE *', required=True, default=fields.Date.today)
    responsible_person_id = fields.Many2one(
        'res.users',
        string='RESPONSIBLE PERSON *',
        required=True,
        default=lambda self: self.env.user
    )
    report_ready_date = fields.Date(string='WHEN WILL REPORT BE READY?*', required=True)
    is_ready = fields.Boolean(string='IS IT READY?*', default=False)
    notes = fields.Text(string='Notes')
    
    # File attachment handling
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'stakeholder_engagement_line_attachment_rel',
        'line_id',
        'attachment_id',
        string='Files'
    )
    
    # ADD THIS FIELD - Report attachment (Many2many to ir.attachment)
    report_attachment_ids = fields.Many2many(
        'ir.attachment',
        'stakeholder_engagement_line_report_rel',
        'line_id',
        'attachment_id',
        string='ATTACH REPORT'
    )
    
    # Remove these if they exist
    # report_attachment = fields.Binary(string='ATTACH REPORT', attachment=True)
    # report_filename = fields.Char(string='Report File Name')
    
    @api.model_create_multi
    def create(self, vals_list):
        """Override create method to handle batch creation"""
        return super(StakeholderEngagementLine, self).create(vals_list)