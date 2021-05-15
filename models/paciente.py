# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import UserError


class HospitalPaciente(models.Model):
    _name = 'odoo_hospital.paciente'
    _description = 'Pacientes del Hospital'

    name = fields.Char(string='Nombre y Apellido', required=True)
    dni = fields.Integer(string='DNI', required=True)
    cantidad_consultas = fields.Integer(string='Cantidad de Consultas', required=True)
    tratamiento_realizado_ids = fields.One2many('odoo_hospital.tratamiento_paciente', 'tratamiento_id',
                                                string='Tratamientos Realizados')

    _sql_constraints = [('dni_unique', 'unique(dni)', 'Paciente con ese DNI existente.')]


class HospitalTratamientoPaciente(models.Model):
    _name = 'odoo_hospital.tratamiento_paciente'
    _description = 'Tratamiento de un Paciente del Hospital'

    tratamiento_id = fields.Many2one('odoo_hospital.paciente', string='Paciente', ondelete='cascade')

    tratamiento = fields.Many2one('odoo_hospital.tratamiento', string='Tratamiento', required=True)
    cantidad = fields.Integer(string='Cantidad', required=True, default=1)

    @api.model
    def create(self, vals):
        tratamiento_paciente = super(HospitalTratamientoPaciente, self).create(vals)
        if tratamiento_paciente.cantidad > 0:
            tratamiento_paciente.tratamiento.veces_solicitado += tratamiento_paciente.cantidad
        else:
            raise UserError('El tratamiento debe tener al menos 1 sesión')
        return tratamiento_paciente

    def write(self, vals):
        if vals.get('cantidad'):
            self.tratamiento.veces_solicitado -= self.cantidad
            self.tratamiento.veces_solicitado += vals.get('cantidad')
        return super(HospitalTratamientoPaciente, self).write(vals)

    @api.multi
    def unlink(self):
        self.tratamiento.veces_solicitado -= self.cantidad
        return super(HospitalTratamientoPaciente, self).unlink()
