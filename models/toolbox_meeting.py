from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class ToolboxMeeting(models.Model):
    _name = 'toolbox.meeting'
    _description = 'Toolbox Meeting'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, time desc'

    # General Information
    name = fields.Char(string='Topic', required=True, tracking=True)
    facilitator = fields.Char(string='Facilitator', tracking=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today, tracking=True)
    time = fields.Float(string='Time', required=True, tracking=True)
    project_id = fields.Many2one('project.project', string='Project', required=True, tracking=True)
    project_site = fields.Char(string='Project Site', tracking=True)
    
    # Related Models (Notebook Tabs)
    attendance_ids = fields.One2many(
        'toolbox.attendance', 
        'meeting_id', 
        string='Attendance Records'
    )
    
    discussion_ids = fields.One2many(
        'toolbox.discussion', 
        'meeting_id', 
        string='Discussion Points'
    )
    
    note_ids = fields.One2many(
        'toolbox.note', 
        'meeting_id', 
        string='Meeting Notes'
    )
    
    file_ids = fields.One2many(
        'toolbox.file', 
        'meeting_id', 
        string='Meeting Files'
    )
    
    # Computed fields
    display_name = fields.Char(string='Display Name', compute='_compute_display_name')
    attendees_count = fields.Integer(string='Attendees', compute='_compute_attendees_count')
    discussions_count = fields.Integer(string='Discussions', compute='_compute_discussions_count')
    notes_count = fields.Integer(string='Notes', compute='_compute_notes_count')
    files_count = fields.Integer(string='Files', compute='_compute_files_count')
    
    @api.depends('name', 'date')
    def _compute_display_name(self):
        for record in self:
            if record.name and record.date:
                record.display_name = f"{record.name} - {record.date}"
            else:
                record.display_name = record.name or 'New Toolbox Meeting'
    
    @api.depends('attendance_ids')
    def _compute_attendees_count(self):
        for record in self:
            record.attendees_count = len(record.attendance_ids)
    
    @api.depends('discussion_ids')
    def _compute_discussions_count(self):
        for record in self:
            record.discussions_count = len(record.discussion_ids)
    
    @api.depends('note_ids')
    def _compute_notes_count(self):
        for record in self:
            record.notes_count = len(record.note_ids)
    
    @api.depends('file_ids')
    def _compute_files_count(self):
        for record in self:
            record.files_count = len(record.file_ids)

    def action_save(self):
        """Persist current changes and keep the user on the form for this record.

        The client normally saves form data automatically, but when a header
        button calls a server method we return the form action for the current
        record so the client navigates to the saved record (discarding any
        client-side draft if the user navigated away).
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_cancel(self):

        action = self.env['ir.actions.act_window'].search(
            [('res_model', '=', 'toolbox.meeting')], limit=1
        )
        if action:
            return action.read()[0]
        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]
        
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('toolbox.meeting') or 'New'
        
        return super().create(vals_list)