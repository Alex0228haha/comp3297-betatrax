from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .services import ProductOwnerService


class POApproveDefect(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, defect_id):
        po_service = ProductOwnerService(request.user)
        if not po_service.product:
            return Response({'error': 'User is not a Product Owner'}, status=status.HTTP_403_FORBIDDEN)

        result = po_service.accept_and_approve_defect(
            report_id=defect_id,
            severity=request.data.get('severity'),
            priority=request.data.get('priority'),
            backlog_item_id=request.data.get('backlog_item_id')
        )

        if result['success']:
            return Response(result)
        return Response(result, status=status.HTTP_400_BAD_REQUEST)


class POResolveDefect(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, defect_id):
        po_service = ProductOwnerService(request.user)
        if not po_service.product:
            return Response({'error': 'User is not a Product Owner'}, status=status.HTTP_403_FORBIDDEN)

        result = po_service.resolve_defect(defect_id)

        if result['success']:
            return Response(result)
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
