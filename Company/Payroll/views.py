from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SalaryDetails, Payslip
from Documents.models import Document
from Employee.models import Employee
from django.contrib import messages
from Notifications.utils import send_notification

@login_required
def payroll_dashboard(request):
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        messages.error(request, "You do not have an Employee profile assigned to your account.")
        return redirect('home')

    # Handle document upload POST
    if request.method == 'POST' and request.FILES.get('document_file'):
        doc_type = request.POST.get('document_type')
        doc_file = request.FILES.get('document_file')
        if doc_type and doc_file:
            Document.objects.create(
                employee=employee,
                document_type=doc_type,
                file=doc_file
            )
            messages.success(request, "Document uploaded successfully!")
        else:
            messages.error(request, "Please provide both document type and file.")
        return redirect('payroll_dashboard')

    # Fetch salary details (graceful default if none exists)
    salary_details = SalaryDetails.objects.filter(employee=employee).first()

    # Calculate net salary
    net_salary = 0
    if salary_details:
        net_salary = salary_details.base_salary + salary_details.bonus - salary_details.deductions

    # Fetch payslips
    payslips = Payslip.objects.filter(employee=employee).order_by('-year', '-month')

    # Fetch uploaded documents
    documents = Document.objects.filter(employee=employee).order_by('-uploaded_at')

    return render(request, 'payroll/dashboard.html', {
        'employee': employee,
        'salary_details': salary_details,
        'net_salary': net_salary,
        'payslips': payslips,
        'documents': documents,
    })

@login_required
def manage_payroll(request):
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        messages.error(request, "Access denied.")
        return redirect('home')

    if employee.employee_role not in ['Admin', 'Manager']:
        messages.error(request, "Only Admins and Managers can access the payroll management console.")
        return redirect('payroll_dashboard')

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_salary':
            emp_id = request.POST.get('employee_id')
            base = request.POST.get('base_salary')
            bonus = request.POST.get('bonus', 0)
            deductions = request.POST.get('deductions', 0)
            
            target_emp = Employee.objects.filter(id=emp_id).first()
            if target_emp and base:
                salary_details, created = SalaryDetails.objects.get_or_create(employee=target_emp, defaults={
                    'base_salary': base,
                    'bonus': bonus,
                    'deductions': deductions
                })
                if not created:
                    salary_details.base_salary = base
                    salary_details.bonus = bonus
                    salary_details.deductions = deductions
                    salary_details.save()
                messages.success(request, f"Salary updated successfully for {target_emp.employee_name}!")
            else:
                messages.error(request, "Invalid salary parameters.")

        elif action == 'upload_payslip':
            emp_id = request.POST.get('employee_id')
            month = request.POST.get('month')
            year = request.POST.get('year')
            payslip_file = request.FILES.get('payslip_file')
            
            target_emp = Employee.objects.filter(id=emp_id).first()
            if target_emp and month and year and payslip_file:
                Payslip.objects.create(
                    employee=target_emp,
                    month=month,
                    year=year,
                    file=payslip_file
                )
                messages.success(request, f"Payslip uploaded successfully for {target_emp.employee_name}!")
                send_notification(
                    recipient=target_emp,
                    title=f"Payslip Available — {month} {year} 💰",
                    message=f"Your payslip for {month} {year} has been uploaded. Visit the Payroll portal to download it.",
                    category='payroll',
                )
            else:
                messages.error(request, "Please provide all details and file for the payslip.")

        return redirect('manage_payroll')

    # Fetch all employees and their salary details
    employees = Employee.objects.all().select_related('salarydetails').order_by('employee_name')
    for emp in employees:
        try:
            sal = emp.salarydetails
            emp.net_salary = sal.base_salary + sal.bonus - sal.deductions
        except SalaryDetails.DoesNotExist:
            emp.net_salary = None

    return render(request, 'payroll/manage.html', {
        'employee': employee,
        'employees': employees,
    })


