from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import DefectReport, Developer, Product
import json


@login_required
@require_http_methods(["GET"])
def list_open_defects(request):
    """
    List all open defects (status='Open') available for the developer to take responsibility for.
    The developer must be associated with a product.
    """
    try:
        # Get the developer associated with the logged-in user
        developer = Developer.objects.get(user=request.user)
    except Developer.DoesNotExist:
        return JsonResponse(
            {'error': 'User is not a registered developer'},
            status=403
        )
    
    # Get all open defects for the developer's product
    open_defects = DefectReport.objects.filter(
        product=developer.product,
        status='Open'
    ).values('id', 'title', 'description', 'severity', 'priority', 'created_at')
    
    return JsonResponse({
        'product': developer.product.name,
        'open_defects': list(open_defects),
        'count': open_defects.count()
    })


@login_required
@require_http_methods(["POST"])
def take_responsibility(request, defect_id):
    """
    Developer takes responsibility for a defect.
    Changes status from 'Open' to 'Assigned' and links the defect to the developer.
    """
    try:
        developer = Developer.objects.get(user=request.user)
    except Developer.DoesNotExist:
        return JsonResponse(
            {'error': 'User is not a registered developer'},
            status=403
        )
    
    # Get the defect report
    defect = get_object_or_404(DefectReport, id=defect_id)
    
    # Verify the defect belongs to the developer's product
    if defect.product != developer.product:
        return JsonResponse(
            {'error': 'Defect does not belong to your product'},
            status=403
        )
    
    # Verify the defect status is 'Open'
    if defect.status != 'Open':
        return JsonResponse(
            {'error': f'Defect status must be Open, currently {defect.status}'},
            status=400
        )
    
    # Update the defect status and assign to developer
    defect.status = 'Assigned'
    defect.assigned_developer = developer
    defect.save()
    
    return JsonResponse({
        'success': True,
        'message': f'You have taken responsibility for defect {defect_id}',
        'defect': {
            'id': defect.id,
            'title': defect.title,
            'status': defect.status,
            'assigned_to': developer.user.username
        }
    })


@login_required
@require_http_methods(["GET"])
def view_defect_detail(request, defect_id):
    """
    View details of a specific defect report.
    Developer can view any defect in their product; other users can only view if assigned to them.
    """
    try:
        developer = Developer.objects.get(user=request.user)
    except Developer.DoesNotExist:
        return JsonResponse(
            {'error': 'You are not a registered developer'},
            status=403
        )
    
    defect = get_object_or_404(DefectReport, id=defect_id)
    
    # Verify access: developer can view defects from their product
    if defect.product != developer.product:
        return JsonResponse(
            {'error': 'You do not have access to this defect'},
            status=403
        )
    
    return JsonResponse({
        'id': defect.id,
        'title': defect.title,
        'description': defect.description,
        'steps_to_reproduce': defect.steps_to_reproduce,
        'product': defect.product.name,
        'tester_id': defect.tester_id,
        'tester_email': defect.tester_email,
        'status': defect.status,
        'severity': defect.severity,
        'priority': defect.priority,
        'assigned_developer': defect.assigned_developer.user.username if defect.assigned_developer else None,
        'created_at': defect.created_at.isoformat(),
        'updated_at': defect.updated_at.isoformat()
    })


@login_required
@require_http_methods(["POST"])
def mark_as_fixed(request, defect_id):
    """
    Developer marks a defect as Fixed.
    Can only be done if the defect is assigned to the developer.
    """
    try:
        developer = Developer.objects.get(user=request.user)
    except Developer.DoesNotExist:
        return JsonResponse(
            {'error': 'You are not a registered developer'},
            status=403
        )
    
    defect = get_object_or_404(DefectReport, id=defect_id)
    
    # Verify the defect is assigned to this developer
    if defect.assigned_developer != developer:
        return JsonResponse(
            {'error': 'Defect is not assigned to you'},
            status=403
        )
    
    # Verify the defect status is 'Assigned'
    if defect.status != 'Assigned':
        return JsonResponse(
            {'error': f'Defect status must be Assigned, currently {defect.status}'},
            status=400
        )
    
    # Update the defect status to 'Fixed'
    defect.status = 'Fixed'
    defect.save()
    
    return JsonResponse({
        'success': True,
        'message': f'Defect {defect_id} marked as Fixed',
        'defect': {
            'id': defect.id,
            'title': defect.title,
            'status': defect.status
        }
    })


@login_required
@require_http_methods(["POST"])
def mark_as_cannot_reproduce(request, defect_id):
    """
    Developer marks a defect as Cannot Reproduce.
    Can only be done if the defect is assigned to the developer.
    """
    try:
        developer = Developer.objects.get(user=request.user)
    except Developer.DoesNotExist:
        return JsonResponse(
            {'error': 'You are not a registered developer'},
            status=403
        )
    
    defect = get_object_or_404(DefectReport, id=defect_id)
    
    # Verify the defect is assigned to this developer
    if defect.assigned_developer != developer:
        return JsonResponse(
            {'error': 'Defect is not assigned to you'},
            status=403
        )
    
    # Verify the defect status is 'Assigned'
    if defect.status != 'Assigned':
        return JsonResponse(
            {'error': f'Defect status must be Assigned, currently {defect.status}'},
            status=400
        )
    
    # Update the defect status to 'Cannot Reproduce'
    defect.status = 'Cannot Reproduce'
    defect.save()
    
    return JsonResponse({
        'success': True,
        'message': f'Defect {defect_id} marked as Cannot Reproduce',
        'defect': {
            'id': defect.id,
            'title': defect.title,
            'status': defect.status
        }
    })
