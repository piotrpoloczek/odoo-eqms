# -*- coding: utf-8 -*-
import functools
import base64
import json
import logging
import os
from odoo import _
from odoo.http import Controller, route, request, Response
import copy
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT

def webservice(f):
    @functools.wraps(f)
    def wrap(*args, **kw):
        try:
            return f(*args, **kw)
        except Exception as e:
            logging.error(e)
            return Response(response=f"{e}", status=500)
    return wrap

class UploadDocument(Controller):

    @route('/plm_document_upload/isalive', type='http', auth='none', methods=['GET'], csrf=False)
    @webservice
    def isalive(self):
        return Response('True', status=200)

    @route('/plm_document_upload/login', type='http', auth='none', methods=['POST'], csrf=False)
    @webservice
    def login(self,
              login,
              password,
              db=None):
        if db and db != request.db:
            raise Exception(_("Could not select database '%s'") % db)
        credential = {'type': 'password', 'login': login, 'password': password}
        uid = request.session.authenticate(request.db, credential )
        if not uid:
            return Response(response="Wrong login/password", status=401)
        return Response(headers={
            'X-CSRF-TOKEN': request.csrf_token(),
        })

    @route('/plm_document_upload/upload_pdf', type='http', auth='user', methods=['POST'], csrf=False)
    @webservice
    def upload_pdf(self,
                   file_stream=None,
                   doc_id=False,
                   **kw):
        logging.info('start upload PDF %r' % (doc_id))
        if doc_id:
            logging.info('start json %r' % (doc_id))
            doc_id = json.loads(doc_id)
            logging.info('start write %r' % (doc_id))
            value1 = file_stream.stream.read()
            request.env['ir.attachment'].browse(doc_id).write(
                {'printout': base64.b64encode(value1),
                 })
            logging.info('upload %r' % (doc_id))
            return Response('Upload succeeded', status=200)
        logging.info('no upload %r' % (doc_id))
        return Response('Failed upload', status=400)

    @route('/plm_document_upload/upload', type='http', auth='user', methods=['POST'], csrf=False)
    @webservice
    def upload(self,
               mod_file=None,
               doc_id=False,
               filename='',
               **kw):
        logging.info('start upload %r' % (doc_id))
        if doc_id:
            logging.info('start json %r' % (doc_id))
            doc_id = json.loads(doc_id)
            logging.info('start write %r' % (doc_id))
            value1 = mod_file.stream.read()
            to_write = {'datas': base64.b64encode(value1),
                        'name': filename}
            preview = kw.get('preview', '')
            if preview:
                to_write['preview'] = base64.b64encode(preview.stream.read())
            ir_attachment_id = request.env['ir.attachment'].browse(doc_id)
            ir_attachment_id.write(to_write)
            ir_attachment_id.sudo().update_component_preview()
            ir_attachment_id.setupCadOpen(kw.get('hostname', ''), kw.get('hostpws', ''), operation_type='save')
            logging.info('upload %r' % (doc_id))
            return Response('Upload succeeded', status=200)
        logging.info('no upload %r' % (doc_id))
        return Response('Failed upload', status=400)

    @route('/plm_document_upload/download', type='http', auth='user', methods=['GET'])
    @webservice
    def download(self,
                 requestvals='[[],[],-1]',
                 **kw):
        logging.info('Download with arguments %r kw %r' % (requestvals, kw))
        if not requestvals:
            logging.info('No file requests to download')
            return Response([], status=200)
        requestvals = json.loads(requestvals)
        ir_attachment = request.env['ir.attachment']
        result = ir_attachment.GetSomeFiles(requestvals)
        docContent = ''
        result2 = {}
        for docTuple in result:
            docId, docName, docContent, checkOutByMe, timeDoc = docTuple
            if not docContent:
                docContent = ''
                docTuple = (docId, docName, docContent, checkOutByMe, timeDoc)
            result2 = copy.deepcopy(list(docTuple))
            docContent = result2[2]
            result2[2] = ''
            break
        return Response(docContent,
                        headers={'result': [result2]})

    @route('/plm_document_upload/upload_preview', type='http', auth='user', methods=['POST'], csrf=False)
    @webservice
    def upload_preview(self,
                       mod_file=None,
                       doc_id=False,
                       **kw):
        logging.info('start upload preview %r' % (doc_id))
        if doc_id:
            logging.info('start json %r' % (doc_id))
            doc_id = json.loads(doc_id)
            logging.info('start write %r' % (doc_id))
            value1 = mod_file.stream.read()
            request.env['ir.attachment'].browse(doc_id).write(
                {'preview': base64.b64encode(value1),
                 })
            logging.info('upload %r' % (doc_id))
            return Response('Upload succeeded', status=200)
        logging.info('no upload %r' % (doc_id))
        return Response('Failed upload', status=400)

    @route('/plm_document_upload/zip_archive', type='http', auth='user', methods=['POST'], csrf=False)
    @webservice
    def upload_zip(self,
                   attachment_id=None,
                   filename='', **kw):
        logging.info('start upload zip %r' % (attachment_id))
        if attachment_id:
            attachment_id = json.loads(attachment_id)
            value1 = kw.get('file_stream').stream.read()
            from_ir_attachment_id = request.env['ir.attachment'].browse(attachment_id)
            zip_name, _zipExtention = os.path.splitext(filename)
            zip_ir_attachment_id  = request.env['ir.attachment'].search([('engineering_code',  'in', [zip_name, filename]),
                                                                         ('engineering_revision', '=', from_ir_attachment_id.engineering_revision),
                                                                         ('document_type', '=', 'other'),
                                                                         ('name', '=', filename)
                                                                         ])
            to_write = {'datas': base64.b64encode(value1),
                        'name': filename,
                        'engineering_code': zip_name,
                        'engineering_revision': from_ir_attachment_id.engineering_revision}
            link_id =  request.env['ir.attachment.relation']
            new_context = request.env.context.copy()
            new_context['backup'] = False
            new_context['check'] = False    # Or zip file will not be updated if in check-in
            contex_brw = request.env['ir.attachment'].with_context(new_context)
            to_write['is_plm'] = True
            if not zip_ir_attachment_id:
                if from_ir_attachment_id.engineering_code == zip_name:
                    to_write['engineering_code'] = filename
                zip_ir_attachment_id  = contex_brw.create(to_write)
            else:
                del to_write['name']
                del to_write['engineering_code']
                del to_write['engineering_revision']
                zip_ir_attachment_id.with_context(new_context).write(to_write)
                link_id = link_id.search([('parent_id', '=', from_ir_attachment_id.id),
                                          ('child_id', '=', zip_ir_attachment_id.id),
                                          ('link_kind', '=', 'PkgTree')])
            if not link_id:
                request.env['ir.attachment.relation'].create({'parent_id': from_ir_attachment_id.id,
                                                              'child_id': zip_ir_attachment_id.id,
                                                              'link_kind': 'PkgTree'})
            return Response('Zip Upload succeeded', status=200)
        logging.info('Zip no upload %r' % (attachment_id))
        return Response('Zip Failed upload', status=400)

    @route('/plm_document_upload/get_zip_archive', type='http', auth='user', methods=['get'], csrf=False)
    @webservice
    def download_zip(self, ir_attachment_id=None, **kw):
        ir_attachment_id = json.loads(ir_attachment_id)
        attachment = request.env['ir.attachment']
        pkg_ids = attachment.getRelatedPkgTree(ir_attachment_id)
        for pkg_id in pkg_ids:
            pkg_brws = attachment.browse(pkg_id)
            return Response(pkg_brws.datas,
                            headers={'file_name': pkg_brws.name})
        return Response(status=200)

    @route('/plm_document_upload/get_files_write_time', type='http', auth='user', methods=['get'], csrf=False)
    @webservice
    def get_files_write_time(self,
                             ir_attachment_ids=None,
                             **kw):
        ir_attachment_ids = json.loads(ir_attachment_ids)
        attachment = request.env['ir.attachment']
        out = []
        for attachment_id in attachment.search([('id','in',ir_attachment_ids)]):
            if attachment_id._is_checkedout_for_me():
                out.append((attachment_id.id,
                            attachment_id.name,
                            attachment_id.write_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)))
        try:
            out = json.dumps(out)
        except Exception as ex:
            logging.error(f"Error dumps object {out}")
            out = json.dumps([])
        return Response(out)


    @route('/plm_document_upload/extra_file', type='http', auth='user', methods=['POST'], csrf=False)
    @webservice
    def upload_extra_file(self,
                          product_id='',
                          doc_name='',
                          doc_rev='0',
                          related_attachment_id='',
                          **kw):
        logging.info('Start upload extra file %r' % (product_id))
        product_id = eval(product_id)
        doc_rev = eval(doc_rev)
        related_attachment_id = eval(related_attachment_id)
        if doc_name:
            value1 = kw.get('file_stream').stream.read()
            ir_attachment_id  = request.env['ir.attachment'].search([('engineering_code',  '=', doc_name),
                                                                     ('engineering_revision', '=', doc_rev)])
            to_write = {'datas': base64.b64encode(value1),
                        'name': kw.get('filename') or doc_name,
                        'engineering_code': doc_name,
                        'engineering_revision': doc_rev}
            link_id =  request.env['ir.attachment.relation']
            new_context = request.env.context.copy()
            new_context['backup'] = False
            new_context['check'] = False    # Or zip file will not be updated if in check-in
            contex_brw = request.env['ir.attachment'].with_context(new_context)
            to_write['is_plm'] = True
            if not ir_attachment_id:
                ir_attachment_id = contex_brw.create(to_write)
            else:
                ir_attachment_id.with_context(new_context).write(to_write)
            if ir_attachment_id and related_attachment_id:
                link_id = link_id.search([('parent_id', '=', related_attachment_id),
                                          ('child_id', '=', ir_attachment_id.id),
                                          ('link_kind', '=', 'ExtraTree')])
            if not link_id:
                request.env['ir.attachment.relation'].create({'parent_id': related_attachment_id,
                                                              'child_id': ir_attachment_id.id,
                                                              'link_kind': 'ExtraTree'})
            if product_id:
                product_id = request.env['product.product'].browse(product_id)
                request.env['plm.component.document.rel'].createFromIds(product_id, ir_attachment_id)
            else:
                if related_attachment_id:
                    for product_id in request.env['ir.attachment'].browse(related_attachment_id).linkedcomponents:
                        request.env['plm.component.document.rel'].createFromIds(product_id, ir_attachment_id)
                        break
            return Response('Extra file Upload succeeded', status=200)
        logging.info('Extra file no upload %r' % (ir_attachment_id))
        return Response('Extra file Failed upload', status=400)

    @route('/plm/ir_attachment_preview/<int:id>', type='http', auth='user', methods=['GET'], csrf=False)
    @webservice
    def get_preview(self, id):
        ir_attachement = request.env['ir.attachment'].sudo()
        for record in ir_attachement.search_read([('id','=', id)], ['preview']):
            return base64.b64decode(record.get('preview'))

    @route('/plm/product_product_image_1920/<int:id>', type='http', auth='user', methods=['GET'], csrf=False)
    @webservice
    def get_product_preview(self, id):
        productobj = request.env['product.product'].sudo()
        for record in productobj.search_read([('id', '=', id)], ['image_1920']):
            return base64.b64decode(record.get('image_1920'))

    @route('/plm/product_product_preview/<int:product_id>', type='http', auth='user', methods=['GET'], csrf=False)
    @webservice
    def get_pp_preview(self, product_id):
        product_product_sudo = request.env['product.product'].sudo()
        for product_product_id in product_product_sudo.search([('id','=', product_id)]):
            return base64.b64decode(product_product_id.image_1920)

    @route('/plm/ir_attachment_printout/<int:id>', type='http', auth='user', methods=['GET'], csrf=False)
    @webservice
    def get_printout(self, id):
        try:
            for ir_attachement_id in request.env['ir.attachment'].sudo().browse(id):
                if ir_attachement_id.printout:
                    print_out_data = request.env['report.plm.ir_attachment_pdf']._render_qweb_pdf(ir_attachement_id)
                    print_out_data = print_out_data[0]
                    if print_out_data:
                        headers = [('Content-Type', 'application/pdf'),
                                   ('Content-Length', len(print_out_data)),
                                   ('Content-Disposition', f'inline; filename="{ir_attachement_id.engineering_code}_{ir_attachement_id.engineering_revision}.pdf"')]
                        return request.make_response(print_out_data, headers)
                    else:
                        return request.not_found(f"Pdf document {ir_attachement_id.engineering_code} not Available")
                else:
                    return request.not_found(f"Pdf document {ir_attachement_id.engineering_code} not Available")
        except Exception as ex:
            return Response(f"{ex}", status=500)
