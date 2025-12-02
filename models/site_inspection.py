from odoo import models, fields, api
from datetime import date

class SiteInspection(models.Model):
    _name = 'site.inspection'
    _description = 'Site Inspection Report'
    
    # General Information
    report_id= fields.Char(string='ID', default='To Be Generated', readonly=True)

    project_id = fields.Many2one('project.project', string='PROJECT', required=True)
    person_responsible = fields.Many2one('hr.employee', string='PERSON RESPONSIBLE', required=True)
    inspected_by = fields.Many2one('hr.employee', string='INSPECTED BY')
    
    # Checks Section
    previous_nc_deviation = fields.Float(string='PREVIOUS NC DEVIATION(%)')
    previous_nc_compliance = fields.Boolean(string='PREVIOUS NC COMPLIANCE')
    previous_nc_availability = fields.Boolean(string='PREVIOUS NC AVAILABILITY')



    previous_nc_remarks = fields.Text(string='PREVIOUS NC REMARKS')
    
    # Additional Comment
    additional_comment = fields.Text(string='COMMENT')
    
    # Files Section
    attachment_ids = fields.Many2many('ir.attachment', string='ATTACH FILE')
    notes = fields.Text(string='Notes')
    
    # Project Details
    project_manager = fields.Many2one('hr.employee', string='PROJECT MANAGER')
    project_consultant = fields.Many2one('hr.employee', string='PROJECT CONSULTANT')
    date_of_inspection = fields.Date(string='DATE OF INSPECTION', default=fields.Date.today)
    
    # Inspection & Test Plan
    inspection_deviation = fields.Float(string='INSPECTION & TEST PLAN DEVIATION (%)')
    inspection_compliance = fields.Boolean(string='INSPECTION & TEST PLAN COMPLIANCE')  
    inspection_availability = fields.Boolean(string='INSPECTION & TEST PLAN AVAILABILITY')
    inspection_remarks = fields.Text(string='INSPECTION & TEST PLAN REMARKS')
    
    # Help Section (Computed/Display Fields)
    inspector_designation = fields.Char(
        string='Inspector Designation',
        compute='_compute_inspector_info',
        readonly=True
    )
    company_info = fields.Char(
        string='Company Information',
        compute='_compute_inspector_info',
        readonly=True
    )
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
    ], string='Status', default='draft')

    attachment_ids = fields.Many2many('ir.attachment', string='Attached Files')
    notes = fields.Text(string='Notes')
    folder_size_kb = fields.Float(string='Folder Size (KB)', compute='_compute_folder_size')
    last_modified_file = fields.Char(string='Last Modified File', compute='_compute_file_info')
    file_type = fields.Char(string='File Type', compute='_compute_file_info')
    
    @api.depends('inspected_by')
    def _compute_inspector_info(self):
        for record in self:
            # Default values
            record.inspector_designation = 'Calibration Specialist'
            record.company_info = 'The Automation Ghana Group Ltd (Provisioning) - PPA SHEQ'
            
            # Could compute based on user if needed
            # if record.inspected_by and record.inspected_by.employee_id:
            #     if record.inspected_by.employee_id.job_id:
            #         record.inspector_designation = record.inspected_by.employee_id.job_id.name
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'To Be Generated') == 'To Be Generated':
                sequence = self.env['ir.sequence'].next_by_code('site.inspection.sequence')
                vals['name'] = sequence or 'New'
        return super().create(vals_list)
    
    def action_save(self):
        if self.report_id == 'To Be Generated':
            self.report_id = 'SIR/' + str(self.id).zfill(4)
        return True
    
    def action_submit(self):
        self.write({'state': 'submitted'})
        return True
    
    def action_approve(self):
        self.write({'state': 'approved'})
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