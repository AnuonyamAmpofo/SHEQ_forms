from odoo import models, fields, api

class ToolboxNote(models.Model):
    _name = 'toolbox.note'
    _description = 'Toolbox Meeting Notes'
    _order = 'sequence, id'

    meeting_id = fields.Many2one('toolbox.meeting', string='Meeting', required=True, ondelete='cascade')
    title = fields.Char(string='Note Title', required=True)
    content = fields.Html(string='Content')
    note_type = fields.Selection([
        ('safety', 'Safety Point'),
        ('quality', 'Quality Point'),
        ('general', 'General Note'),
        ('action', 'Action Item')
    ], string='Type', default='general')
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string='Priority', default='medium')
    sequence = fields.Integer(string='Sequence', default=10)