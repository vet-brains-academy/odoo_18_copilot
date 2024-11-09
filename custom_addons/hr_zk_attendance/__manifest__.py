{
    'name': 'Biometric Device Integration',
    'version': '18.0.1.0.0',  # Updated version number to match Odoo 18
    'summary': """Integrating Biometric Device (Model: ZKteco uFace 202) With HR Attendance (Face + Thumb)""",
    'description': """This module integrates Odoo with the biometric device(Model: ZKteco uFace 202)""",
    'category': 'Human Resources/Attendance',  # Updated category path
    'author': 'Cybrosys Techno Solutions, Mostafa Shokiel',
    'company': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'depends': [
        'base_setup',
        'hr_attendance',  # Changed from attendance_timesheet to hr_attendance
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/zk_machine_view.xml',
        'views/zk_machine_attendance_view.xml',
        'data/download_data.xml'
    ],
    'assets': {  # Add assets if you have any JS/CSS files
        'web.assets_backend': [
            # 'hr_zk_attendance/static/src/js/*.js',
            # 'hr_zk_attendance/static/src/css/*.css',
        ],
    },
    'images': ['static/description/banner.gif'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}