# -*- coding: utf-8 -*-

from openerp.osv import osv,fields
from openerp import SUPERUSER_ID
from stj_base.osv import osv as base_osv


class document_directory(base_osv.Model):
    _name = 'document.directory'
    _inherit = 'document.directory'
    _columns = {
        'personal_active': fields.boolean('有效'),
        'is_root': fields.boolean('root目录'),
    }
    _defaults = {
        'personal_active': True,
    }

document_directory()