from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status


class CrearExpedientesPermission(permissions.BasePermission):
    # No podemos llamarla diferente a "has_permission"
    def has_permission(self, request, view):
        
        # VERIFICAR QUE SE PROPORCIONÓ UN TOKEN
        if request.auth:
            # Verificar el permiso específico (crear_expedientes)
            crear_expedientes_permission = bool(request.user and request.user.crear_expedientes)
            return crear_expedientes_permission
        else:
            return False


class CargaMasivaPermission(permissions.BasePermission):
    # No podemos llamarla diferente a "has_permission"
    def has_permission(self, request, view):
        
        # VERIFICAR QUE SE PROPORCIONÓ UN TOKEN
        if request.auth:
            # Verificar el permiso específico (crear_expedientes)
            carga_masiva_permission = bool(request.user and request.user.carga_masiva)
            return carga_masiva_permission
        else:
            return False


class RemoveExpedientesPermission(permissions.BasePermission):
    # No podemos llamarla diferente a "has_permission"
    def has_permission(self, request, view):

        # VERIFICAR QUE SE PROPORCIONÓ UN TOKEN
        if request.auth:
            # Verificar el permiso específico (remove_expedientes_permission)
            remove_expedientes_permission = bool(request.user and request.user.eliminar_expedientes)
            return remove_expedientes_permission
        else:
            False


class SubirDocumentosPermission(permissions.BasePermission):
    # No podemos llamarla diferente a "has_permission"
    def has_permission(self, request, view):

        # VERIFICAR QUE SE PROPORCIONÓ UN TOKEN
        if not request.auth:
            return False
        else:
            # TIENE QUE ESTAR LOGEADO Y TENER PERMISO PARA ELIMINAR EXPEDIENTES
            subir_documentos_permission = bool(request.user and request.user.subir_documentos)
            return subir_documentos_permission
        
class DeleteDocumentsPermission(permissions.BasePermission):
    # No podemos llamarla diferente a "has_permission"
    def has_permission(self, request, view):

        # VERIFICAR QUE SE PROPORCIONÓ UN TOKEN
        if not request.auth:
            return False
        else:
            # TIENE QUE ESTAR LOGEADO Y TENER PERMISO PARA ELIMINAR EXPEDIENTES
            delete_documento_permission = bool(request.user and request.user.eliminar_documentos)
            return delete_documento_permission

