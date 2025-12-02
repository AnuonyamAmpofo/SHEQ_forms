from odoo import models, fields, api

class SHEQAudit(models.Model):
    _name = 'sheq.audit'
    _description = 'SHEQ Audit Form'
    
    # Primary Information
    title = fields.Char(string='Title', required=True)
    auditor = fields.Many2one('res.users', string='AUDITOR', required=True, default=lambda self: self.env.user)
    
    # Details section
    audit_type = fields.Char(string='AUDIT TYPE', required=True)
    audit_area = fields.Char(string='AUDIT AREA/PROCESS', required=True)
    audit_start_time = fields.Char(string='AUDIT START TIME', required=True)
    audit_id = fields.Char(string='ID', default='To Be Generated', readonly=True)
    

    note = fields.Text(string='Notes')
    

    lead_auditor = fields.Many2one('hr.employee', string='LEAD AUDITOR', required=True)
    department = fields.Many2one('hr.department', string='DEPARTMENT', required=True)
    auditee = fields.Many2one('hr.employee', string='AUDITEE', required=True)
    subsidiary = fields.Many2one('res.company', string='SUBSIDIARY', default=lambda self: self.env.user.company_id)

   
    subsidiary = fields.Many2one(
    'res.company',
    string='SUBSIDIARY',  
    default=lambda self: self.env.company,  
    required=True
)
    
    # Bottom section
    audit_end_time = fields.Char(string='AUDIT END TIME', required=True)
    audit_date = fields.Date(string='AUDIT DATE', required=True, default=fields.Date.today)
    audit_status = fields.Selection([
        ('open', 'Open'),
        ('closed', 'Closed')
    ], string='AUDIT STATUS', default='open')
    audit_venue = fields.Char(string='AUDIT VENUE')

    attachment_ids = fields.Many2many('ir.attachment', string='Attached Files')
    notes = fields.Text(string='Notes')
    folder_size_kb = fields.Float(string='Folder Size (KB)', compute='_compute_folder_size')
    last_modified_file = fields.Char(string='Last Modified File', compute='_compute_file_info')
    file_type = fields.Char(string='File Type', compute='_compute_file_info')
    
    # Simple actions
    def action_save(self):
        if self.audit_id == 'To Be Generated':
            self.audit_id = 'AUD/' + str(self.id).zfill(4)
        return True
    
    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}

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