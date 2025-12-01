{
    'name': 'TAGG Academy',
    'version': '1.0',
    'summary': 'Incident Register Management for TAGG Academy',
    'category': 'Human Resources',
    'depends': ['base', 'mail', 'hr', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_tagg_objectives.xml',
        'data/ir_sequence_tagg_process_evaluation.xml',
        'data/ir_sequence_tagg_process_request.xml',
        'views/incident_register_views.xml',
        'views/tagg_objectives_views.xml',
        'views/tagg_process_evaluation_views.xml',
        'views/tagg_process_views.xml',
        'views/process_request_views.xml',
        'views/toolbox_meeting_views.xml',
        'views/testing_tool_views.xml',
        'views/sheq_approved_document_views.xml',
        
        'views/tagg_academy_menus.xml',  
        
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}