from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TestingTool(models.Model):
    _name = 'testing.tool'
    _description = 'Testing Tool'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Testing Tool', required=True)
    model = fields.Char(string='Model')
    quantity = fields.Integer(string='Quantity', default=1)
    serial_number = fields.Char(string='Serial Number', required=True)
    
    # Files section
    attachment_ids = fields.Many2many('ir.attachment', string='Attached Files')
    notes = fields.Text(string='Notes')
    
    # Condition and calibration
    condition = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('broken', 'Broken'),
    ], string='Condition', default='good')
    
    last_calibration_date = fields.Date(string='Last Calibration Date', required=True)
    next_calibration_date = fields.Date(string='Next Calibration Date', required=True)
    
    # Collection info (computed fields)
    folder_size_kb = fields.Float(string='Folder Size (KB)', compute='_compute_folder_size')
    last_modified_file = fields.Char(string='Last Modified File', compute='_compute_file_info')
    file_type = fields.Char(string='File Type', compute='_compute_file_info')

    @api.depends('attachment_ids')
    def _compute_folder_size(self):
        for record in self:
            total_size = sum(attachment.file_size for attachment in record.attachment_ids if attachment.file_size)
            record.folder_size_kb = total_size / 1024 if total_size else 0

    @api.depends('attachment_ids')
    def _compute_file_info(self):
        for record in self:
            if record.attachment_ids:
                latest_attachment = max(record.attachment_ids, key=lambda x: x.write_date)
                record.last_modified_file = latest_attachment.name
                record.file_type = latest_attachment.mimetype or 'Unknown'
            else:
                record.last_modified_file = ''
                record.file_type = ''

    
    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)

    # Button methods
    def action_save(self):
        """Save the record"""
        return {'type': 'ir.actions.act_window_close'}

    def action_cancel(self):
        """Cancel and go back"""
        return {'type': 'ir.actions.act_window_close'}

    def action_remove_all_attachments(self):
        """Remove all attached files"""
        self.ensure_one()
        self.attachment_ids = [(5, 0, 0)]
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'All attachments have been removed',
                'type': 'success',
                'sticky': False,
            }
        }

    def action_generate_report(self):
        """Generate a report for the testing tool"""
        self.ensure_one()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Generate Report',
                'message': 'Report generation would create a PDF summary',
                'type': 'info',
                'sticky': False,
            }
        }

    # Validation for required fields
    @api.constrains('name', 'serial_number', 'last_calibration_date', 'next_calibration_date')
    def _check_required_fields(self):
        for record in self:
            if not record.name:
                raise ValidationError("Testing Tool name is required!")
            if not record.serial_number:
                raise ValidationError("Serial Number is required!")
            if not record.last_calibration_date:
                raise ValidationError("Last Calibration Date is required!")
            if not record.next_calibration_date:
                raise ValidationError("Next Calibration Date is required!")