# -*- coding: utf-8 -*-

from odoo import fields, models, api


class HospitalTratamiento(models.Model):
    _name = 'odoo_hospital.tratamiento'
    _description = 'Tratamientos del Hospital'

    name = fields.Char(string='Tratamiento', required=True)
    valor = fields.Float(string='Valor', required=True)
    veces_solicitado = fields.Integer(default=0)

    _sql_constraints = [('tratamiento_unique', 'unique(name)', 'El tratamiento ya existe.')]
