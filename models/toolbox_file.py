from odoo import models, fields, api

class ToolboxFile(models.Model):
    _name = 'toolbox.file'
    _description = 'Toolbox Meeting Files'
    _order = 'sequence, id'

    meeting_id = fields.Many2one('toolbox.meeting', string='Meeting', required=True, ondelete='cascade')
    name = fields.Char(string='File Name', required=True)
    attachment = fields.Binary(string='File', required=True)
    attachment_filename = fields.Char(string='File Name')
    description = fields.Text(string='Description')
    file_type = fields.Selection([
        ('document', 'Document'),
        ('image', 'Image'),
        ('pdf', 'PDF'),
        ('other', 'Other')
    ], string='File Type')
    sequence = fields.Integer(string='Sequence', default=10)