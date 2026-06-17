from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Departments.models import Department
from Employee.models import Employee
from Projects.models import Project, Task

class DepartmentAnalyticsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create department
        self.dept = Department.objects.create(
            department_name="Engineering",
            department_no_of_projects=3,
            department_head="Alice Smith",
            department_region="West"
        )
        
        # Create user & employee
        self.user = User.objects.create_user(username="test_user", password="password123")
        self.emp = Employee.objects.create(
            user=self.user,
            employee_role="Employee",
            employee_name="Test Employee",
            employee_age="26",
            employee_address="456 Tech Lane",
            employee_department="Engineering",
            employee_reporting_manager="Alice Smith",
            employee_email="test_emp@company.com"
        )

        # Create project and tasks
        self.project = Project.objects.create(
            name="Cloud Sync",
            department=self.dept,
            deadline="2026-12-31"
        )
        self.task1 = Task.objects.create(
            project=self.project,
            title="S3 migration",
            status="Completed"
        )
        self.task2 = Task.objects.create(
            project=self.project,
            title="Setup alerts",
            status="In Progress"
        )

    def test_department_analytics_requires_login(self):
        """Verify redirect to login for unauthenticated requests"""
        response = self.client.get(reverse('Department Analytics'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])

    def test_department_analytics_loads_successfully(self):
        """Verify that analytics page renders all key metrics correctly when logged in"""
        self.client.login(username="test_user", password="password123")
        response = self.client.get(reverse('Department Analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Department Analytics")
        self.assertContains(response, "Engineering")
        self.assertContains(response, "Alice Smith")
        # Check headcount and project count are present in data attributes
        self.assertContains(response, 'data-headcount="1"')
        self.assertContains(response, 'data-projects="1"')
        # Check task statuses
        self.assertContains(response, 'data-completed="1"')
        self.assertContains(response, 'data-progress="1"')
