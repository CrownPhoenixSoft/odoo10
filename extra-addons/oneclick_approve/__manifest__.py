
{
    'name': 'One Click Approve',
    'version': '10.0.1.0.0',
    'summary': 'Provides actions in single menu to different model based on their states',
    'category': 'Managment',
    'author': 'Pandoratech',
    'maintainer': 'Pandoratech',
    'company': 'Pandora Desgin',
    'website': 'https://pandoratech.ae',
    'depends': ['stock','sale','purchase',
                #'project',
                'hr_holidays','hr_expense'],
    'data': [
       'views/main_menu.xml',
    ],
    
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
