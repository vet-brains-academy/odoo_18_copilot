{
    'name': 'ZKTeco Face Recognition',
    'version': '18.0.1.0.0',
    'summary': 'Integration with ZKTeco uFace800 Face Recognition Device',
    'description': """
        Integrate Odoo with ZKTeco uFace800 biometric device for attendance management.
        Features:
        - Connect to ZKTeco devices over network
        - Download attendance logs
        - Manage employee biometric data
        - Real-time attendance monitoring
        - Support for face and fingerprint recognition
    """,
    'category': 'Human Resources/Attendance',
    'author': 'Your Company',
    'website': "https://www.yourcompany.com",
    'depends': [
        'base_setup',
        'hr',
        'hr_attendance',
    ],
    'data': [
        'security/zk_security.xml',
        'security/ir.model.access.csv',
        'views/zk_device_view.xml',
        'views/hr_employee_view.xml',
        'views/zk_attendance_view.xml',
        'data/zk_scheduler.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'zk_face_attendance/static/src/js/**/*',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'sequence': 1,
} 