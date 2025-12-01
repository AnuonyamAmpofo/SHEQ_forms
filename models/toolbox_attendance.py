from odoo import models, fields, api

class ToolboxAttendance(models.Model):
    _name = 'toolbox.attendance'
    _description = 'Toolbox Meeting Attendance'
    _order = 'sequence, id'

    meeting_id = fields.Many2one('toolbox.meeting', string='Meeting', required=True, ondelete='cascade')
    name = fields.Char(string='Name', required=True)
    role = fields.Char(string='Role', required=True)
    # signature = fields.Binary(string='Signature')
    # sign_date = fields.Datetime(string='Signed On', default=fields.Datetime.now)
    sequence = fields.Integer(string='Sequence', default=10)
    

    # employee_id = fields.Many2one('hr.employee', string='Employee')