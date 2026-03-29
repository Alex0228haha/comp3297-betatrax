from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import ProductOwnerService

# API: List all New defect reports for PO (UC002)
class PO_NewDefectList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        product_id = request.GET.get('product_id')
        po_service = ProductOwnerService(request.user)
        defects = po_service.get_new_defect_list(product_id)

        data = [{
            "report_id": d.id,
            "title": d.title,
            "tester_id": d.tester_id,
            "submitted_at": d.created_at,
            "status": d.status
        } for d in defects]

        return Response(data)

# API: Get full details of one defect report
class PO_DefectDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        report_id = request.GET.get('report_id')
        product_id = request.GET.get('product_id')
        po_service = ProductOwnerService(request.user)
        defect = po_service.get_defect_detail(report_id, product_id)

        if not defect:
            return Response({"error": "Defect not found"}, status=404)

        return Response({
            "report_id": defect.id,
            "product_id": defect.product.id,
            "title": defect.title,
            "description": defect.description,
            "reproduction_steps": defect.steps_to_reproduce,
            "tester_id": defect.tester_id,
            "tester_email": defect.tester_email,
            "status": defect.status,
            "submitted_at": defect.created_at
        })

# API: Approve defect and update status to Open (UC002 main function)
class PO_ApproveDefect(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        po_service = ProductOwnerService(request.user)
        result = po_service.accept_and_approve_defect(
            report_id=request.data.get('report_id'),
            product_id=request.data.get('product_id'),
            severity=request.data.get('severity'),
            priority=request.data.get('priority'),
            backlog_item_id=request.data.get('backlog_item_id')
        )

        if result["success"]:
            return Response(result)
        return Response(result, status=400)
