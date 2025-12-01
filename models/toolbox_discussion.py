from odoo import models, fields, api

class ToolboxDiscussion(models.Model):
    _name = 'toolbox.discussion'
    _description = 'Toolbox Meeting Discussion Points'
    _order = 'sequence, id'

    meeting_id = fields.Many2one('toolbox.meeting', string='Meeting', required=True, ondelete='cascade')
    topic = fields.Char(string='Discussion Topic', required=True)
    description = fields.Text(string='Details')
    action_required = fields.Boolean(string='Action Required')
    responsible_person = fields.Char(string='Responsible Person')
    deadline = fields.Date(string='Deadline')
    status = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='open')
    sequence = fields.Integer(string='Sequence', default=10)