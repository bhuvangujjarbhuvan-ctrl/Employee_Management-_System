from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from Employee.models import Employee
from Leave.models import Attendance, LeaveRequest
from Projects.models import Project, Task
from Payroll.models import SalaryDetails, Payslip
from Documents.models import Document
from Departments.models import Department
import datetime

class CorpNexusTestCase(TestCase):
    def setUp(self):
        # Create department
        self.dept = Department.objects.create(
            department_name="Engineering",
            department_no_of_projects=5,
            department_head="Bhuvan",
            department_region="North"
        )
        
        # Create users
        self.admin_user = User.objects.create_user(username="admin", password="password123")
        self.emp_user = User.objects.create_user(username="employee", password="password123")
        
        # Create employee profiles
        self.admin_emp = Employee.objects.create(
            user=self.admin_user,
            employee_role="Admin",
            employee_name="Admin User",
            employee_age="30",
            employee_address="HQ",
            employee_department="Engineering",
            employee_reporting_manager="None",
            employee_email="admin@company.com"
        )
        self.regular_emp = Employee.objects.create(
            user=self.emp_user,
            employee_role="Employee",
            employee_name="Regular Employee",
            employee_age="25",
            employee_address="Sub-office",
            employee_department="Engineering",
            employee_reporting_manager="Admin User",
            employee_email="emp@company.com"
        )
        
        # Create projects and tasks
        self.project = Project.objects.create(
            name="Alpha Project",
            department=self.dept,
            deadline=datetime.date.today() + datetime.timedelta(days=30),
            status="In Progress"
        )
        self.task = Task.objects.create(
            project=self.project,
            assigned_employee=self.regular_emp,
            title="Design Phase",
            status="To Do"
        )

        self.client = Client()

    def test_authentication(self):
        # Try accessing dashboard unauthenticated
        response = self.client.get(reverse('leave_dashboard'))
        self.assertEqual(response.status_code, 302) # Redirects to login
        
        # Log in
        login_success = self.client.login(username="employee", password="password123")
        self.assertTrue(login_success)
        
        # Access dashboard now
        response = self.client.get(reverse('leave_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_attendance_and_leaves(self):
        self.client.login(username="employee", password="password123")
        
        # Clock in
        response = self.client.post(reverse('leave_dashboard'), {'action': 'clock_in'})
        self.assertEqual(response.status_code, 302)
        today_att = Attendance.objects.filter(employee=self.regular_emp).first()
        self.assertIsNotNone(today_att)
        self.assertIsNotNone(today_att.clock_in)
        self.assertIsNone(today_att.clock_out)
        
        # Clock out
        response = self.client.post(reverse('leave_dashboard'), {'action': 'clock_out'})
        self.assertEqual(response.status_code, 302)
        today_att.refresh_from_db()
        self.assertIsNotNone(today_att.clock_out)
        
        # Request leave
        response = self.client.post(reverse('leave_dashboard'), {
            'action': 'request_leave',
            'leave_type': 'Sick Leave',
            'start_date': str(datetime.date.today()),
            'end_date': str(datetime.date.today() + datetime.timedelta(days=2))
        })
        self.assertEqual(response.status_code, 302)
        leave = LeaveRequest.objects.filter(employee=self.regular_emp).first()
        self.assertIsNotNone(leave)
        self.assertEqual(leave.status, 'Pending')
        
        # Admin approves leave
        self.client.login(username="admin", password="password123")
        response = self.client.post(reverse('approve_leave', args=[leave.id]), {'action': 'approve'})
        self.assertEqual(response.status_code, 302)
        leave.refresh_from_db()
        self.assertEqual(leave.status, 'Approved')

    def test_projects_and_tasks(self):
        self.client.login(username="employee", password="password123")
        
        # Start task
        response = self.client.post(reverse('projects_dashboard'), {
            'task_id': self.task.id,
            'status': 'In Progress'
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'In Progress')
        
        # Complete task
        response = self.client.post(reverse('projects_dashboard'), {
            'task_id': self.task.id,
            'status': 'Completed'
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'Completed')

    def test_payroll_and_document_uploads(self):
        self.client.login(username="employee", password="password123")
        
        # Upload a dummy document
        test_file = SimpleUploadedFile("resume.pdf", b"pdf content", content_type="application/pdf")
        response = self.client.post(reverse('payroll_dashboard'), {
            'document_type': 'ID Proof',
            'document_file': test_file
        })
        self.assertEqual(response.status_code, 302)
        doc = Document.objects.filter(employee=self.regular_emp).first()
        self.assertIsNotNone(doc)
        self.assertEqual(doc.document_type, 'ID Proof')
        self.assertTrue(doc.file.name.endswith('resume.pdf'))
        
        # Clean up file from filesystem after test
        doc.file.delete()

    def test_rest_api_protection(self):
        # Anonymous user accessing API
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, 403) # Forbidden
        
        # Logged-in user accessing API
        self.client.login(username="employee", password="password123")
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, 200) # Success

    def test_signup(self):
        # Access signup page
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        
        # Post registration data
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password': 'newpassword123',
            'confirm_password': 'newpassword123',
            'employee_name': 'New Employee',
            'employee_age': '28',
            'employee_address': 'New Address',
            'employee_department': 'Engineering',
            'employee_reporting_manager': 'Admin User',
            'employee_email': 'newuser@company.com'
        })
        self.assertEqual(response.status_code, 302) # Redirects to home
        
        # Verify user and employee profile exist
        user_exists = User.objects.filter(username='newuser').exists()
        self.assertTrue(user_exists)
        emp = Employee.objects.filter(employee_email='newuser@company.com').first()
        self.assertIsNotNone(emp)
        self.assertEqual(emp.employee_name, 'New Employee')
        self.assertEqual(emp.user.username, 'newuser')

    def test_payroll_management(self):
        # Access manage payroll unauthenticated
        response = self.client.get('/payroll/manage/')
        self.assertEqual(response.status_code, 302) # Redirects to login
        
        # Access manage payroll as regular employee
        self.client.login(username="employee", password="password123")
        response = self.client.get('/payroll/manage/')
        self.assertEqual(response.status_code, 302) # Redirects to personal dashboard
        
        # Access manage payroll as admin
        self.client.login(username="admin", password="password123")
        response = self.client.get('/payroll/manage/')
        self.assertEqual(response.status_code, 200) # Success
        
        # Post to update salary structure for employee
        response = self.client.post('/payroll/manage/', {
            'action': 'update_salary',
            'employee_id': self.regular_emp.id,
            'base_salary': '6200.00',
            'bonus': '500.00',
            'deductions': '200.00'
        })
        self.assertEqual(response.status_code, 302) # Redirects to self
        
        # Verify SalaryDetails updated
        sal_details = SalaryDetails.objects.filter(employee=self.regular_emp).first()
        self.assertIsNotNone(sal_details)
        self.assertEqual(sal_details.base_salary, 6200.00)
        self.assertEqual(sal_details.bonus, 500.00)
        self.assertEqual(sal_details.deductions, 200.00)
        
        # Post to upload payslip for employee
        test_payslip = SimpleUploadedFile("payslip_may.pdf", b"pdf content", content_type="application/pdf")
        response = self.client.post('/payroll/manage/', {
            'action': 'upload_payslip',
            'employee_id': self.regular_emp.id,
            'month': 'May',
            'year': '2026',
            'payslip_file': test_payslip
        })
        self.assertEqual(response.status_code, 302) # Redirects to self
        
        # Verify Payslip created
        payslip = Payslip.objects.filter(employee=self.regular_emp, month='May', year=2026).first()
        self.assertIsNotNone(payslip)
        self.assertTrue(payslip.file.name.endswith('payslip_may.pdf'))
        
        # Clean up files
        payslip.file.delete()


class EmployeeProfileTestCase(TestCase):
    """Tests for the Employee Profile Page feature."""

    def setUp(self):
        self.client = Client()
        self.dept = Department.objects.create(
            department_name="QA",
            department_no_of_projects=2,
            department_head="Lead",
            department_region="South"
        )
        self.user = User.objects.create_user(username="profile_user", password="pass1234")
        self.employee = Employee.objects.create(
            user=self.user,
            employee_role="Employee",
            employee_name="Profile User",
            employee_age="28",
            employee_address="123 Test St",
            employee_department="QA",
            employee_reporting_manager="Lead",
            employee_email="profile@test.com",
            bio="Hello world",
            phone="1234567890",
            contract_type="Full-Time",
        )
        self.admin_user = User.objects.create_user(username="profile_admin", password="pass1234")
        self.admin_emp = Employee.objects.create(
            user=self.admin_user,
            employee_role="Admin",
            employee_name="Profile Admin",
            employee_age="35",
            employee_address="456 Admin Ave",
            employee_department="IT",
            employee_reporting_manager="CTO",
            employee_email="padmin@test.com",
        )

    def test_my_profile_requires_login(self):
        """Unauthenticated users are redirected to login."""
        response = self.client.get(reverse('my_profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])

    def test_my_profile_loads_for_authenticated_user(self):
        """Authenticated employee can load their own profile."""
        self.client.login(username="profile_user", password="pass1234")
        response = self.client.get(reverse('my_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profile User")

    def test_my_profile_update_bio(self):
        """Employee can update their bio via POST."""
        self.client.login(username="profile_user", password="pass1234")
        response = self.client.post(reverse('my_profile'), {
            'bio': 'Updated bio text',
            'phone': '9876543210',
            'contract_type': 'Part-Time',
            'employee_address': '789 New St',
        })
        self.assertEqual(response.status_code, 302)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.bio, 'Updated bio text')
        self.assertEqual(self.employee.phone, '9876543210')
        self.assertEqual(self.employee.contract_type, 'Part-Time')

    def test_employee_profile_view_by_id(self):
        """Admin can view any employee profile by ID."""
        self.client.login(username="profile_admin", password="pass1234")
        response = self.client.get(reverse('employee_profile', args=[self.employee.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profile User")

    def test_admin_user_management_access(self):
        """Only users with Admin role can access User Management."""
        # Unauthenticated
        response = self.client.get(reverse('admin_user_management'))
        self.assertEqual(response.status_code, 302)

        # Regular Employee
        self.client.login(username="profile_user", password="pass1234")
        response = self.client.get(reverse('admin_user_management'))
        self.assertEqual(response.status_code, 302) # Redirects to home with error

        # Admin
        self.client.login(username="profile_admin", password="pass1234")
        response = self.client.get(reverse('admin_user_management'))
        if response.status_code == 302:
            print("REDIRECT LOCATION:", response['Location'])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User Management")

    def test_admin_user_management_update_role(self):
        """Admin can change employee roles."""
        self.client.login(username="profile_admin", password="pass1234")
        response = self.client.post(reverse('admin_user_management'), {
            'action': 'update_role',
            'emp_id': self.employee.id,
            'role': 'Manager',
        })
        self.assertEqual(response.status_code, 302)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.employee_role, 'Manager')

    def test_admin_user_management_toggle_active(self):
        """Admin can toggle user active status."""
        self.client.login(username="profile_admin", password="pass1234")
        self.assertTrue(self.user.is_active)
        response = self.client.post(reverse('admin_user_management'), {
            'action': 'toggle_active',
            'emp_id': self.employee.id,
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_admin_user_management_reset_password(self):
        """Admin can reset a user's password."""
        self.client.login(username="profile_admin", password="pass1234")
        response = self.client.post(reverse('admin_user_management'), {
            'action': 'reset_password',
            'emp_id': self.employee.id,
            'new_password': 'newpassword123',
        })
        self.assertEqual(response.status_code, 302)
        # Verify login with new password works
        self.client.logout()
        login_success = self.client.login(username="profile_user", password="newpassword123")
        self.assertTrue(login_success)



