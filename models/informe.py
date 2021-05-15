# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import http
from odoo.http import request, content_disposition, route


class HospitalInforme1(models.TransientModel):
    _name = 'odoo_hospital.informe1'


    @api.multi
    def imprimir_reporte(self):

        tratamiento_mas_solicitado = self.env['odoo_hospital.tratamiento'].search([], order='veces_solicitado desc', limit=1)

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/download/informe-hospital?tratamiento_id=%s' % (tratamiento_mas_solicitado.id),
            'report_name': 'odoo_hospital.informe_tratamiento_view',
            'target': 'self',
        }


class HospitalInforme2(models.TransientModel):
    _name = 'odoo_hospital.informe2'

    pacientes_menos_consultas_ids = fields.One2many('odoo_hospital.paciente', compute='set_pacientes_menos_consultas')

    @api.multi
    def set_pacientes_menos_consultas(self):
        for rec in self:
            pacientes_menos_consultas = self.env['odoo_hospital.paciente']
            pacientes = self.env['odoo_hospital.paciente'].search([])
            cantidad_consultas = 0
            for paciente in pacientes:
                cantidad_consultas += paciente.cantidad_consultas

            promedio_consultas = cantidad_consultas / len(pacientes)

            pacientes = self.env['odoo_hospital.paciente'].search([('cantidad_consultas', '<', promedio_consultas)])
            for paciente in pacientes:
                pacientes_menos_consultas += paciente

            rec.pacientes_menos_consultas_ids = pacientes_menos_consultas

    @api.multi
    def imprimir_reporte(self):

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/download/informe-hospital2?paciente_id=%s' % (self.id),
            'report_name': 'odoo_hospital.informe_paciente_view',
            'target': 'self',
        }


class HospitalInforme3(models.TransientModel):
    _name = 'odoo_hospital.informe3'

    porcentaje = fields.Float()

    @api.multi
    def imprimir_reporte(self):

        pacientes = self.env['odoo_hospital.paciente'].search([])
        pacientes_compradores = 0
        for paciente in pacientes:
            if len(paciente.tratamiento_realizado_ids) > 0:
                pacientes_compradores += 1

        self.porcentaje = (pacientes_compradores / len(pacientes)) * 100

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/download/informe-hospital3?paciente_comprador_id=%s' % (self.id),
            'report_name': 'odoo_hospital.informe_paciente_comprador_view',
            'target': 'self',
        }


# Controller para descargar los Informes
class InformeDownload(http.Controller):

    # Informe tratamiento mas solicitado
    @route(['/web/download/informe-hospital'], type='http', auth="user")
    def download_pdf(self, tratamiento_id, **kw):
        tratamiento_mas_solicitado = request.env['odoo_hospital.tratamiento'].sudo().search(
            [('id', '=', tratamiento_id)], limit=1)
        if not tratamiento_mas_solicitado:
            return None
        pdf, _ = request.env.ref('odoo_hospital.informe_tratamiento').sudo().render_qweb_pdf(
            [int(tratamiento_id)])
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf)),
                          ('Content-Disposition',
                           content_disposition('%s - Tratamiento Solicitado.PDF' % (tratamiento_mas_solicitado.name)))]
        return request.make_response(pdf, headers=pdfhttpheaders)

    # Informe pacientes con menos consultas
    @route(['/web/download/informe-hospital2'], type='http', auth="user")
    def download_pdf2(self, paciente_id, **kw):
        pacientes = request.env['odoo_hospital.informe2'].sudo().search(
            [('id', '=', paciente_id)], limit=1)
        if not pacientes:
            return None
        pdf, _ = request.env.ref('odoo_hospital.informe_paciente').sudo().render_qweb_pdf(
            [int(paciente_id)])
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf)),
                          ('Content-Disposition',
                           content_disposition('Pacientes con menos consultas.PDF'))]
        return request.make_response(pdf, headers=pdfhttpheaders)

    # Informe pacientes que compraron al menos 1 tratamiento
    @route(['/web/download/informe-hospital3'], type='http', auth="user")
    def download_pdf3(self, paciente_comprador_id, **kw):
        pacientes = request.env['odoo_hospital.informe3'].sudo().search(
            [('id', '=', paciente_comprador_id)], limit=1)
        if not pacientes:
            return None
        pdf, _ = request.env.ref('odoo_hospital.informe_paciente_comprador').sudo().render_qweb_pdf(
            [int(paciente_comprador_id)])
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf)),
                          ('Content-Disposition',
                           content_disposition('Pacientes compradores.PDF'))]
        return request.make_response(pdf, headers=pdfhttpheaders)