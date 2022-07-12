from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import *
from .serializers import *

class CompanyApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the companies
        '''
        companies = Company.objects.all().values_list()
        return Response(companies, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create a Company
        POST example
        {
            "email": "excompany@google.com",
            "description": "Tech",
            "name": "Google"
        }
        '''
        # check if company exists through email
        email = request.data.get('email')
        if not Company.objects.filter(email = email).exists():
            data = {
                'email': email, 
                'description': request.data.get('description'), 
                'name': request.data.get('name')
            }
            serializer = CompanySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # invalid serializer
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error' : 'Company already exists'}, status=status.HTTP_400_BAD_REQUEST)

class CompanyJobApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the Job skills
        '''
        companyJobs = CompanyJob.objects.all().values_list()
        return Response(companyJobs, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create a Company Job
        POST example
        {
            "email": "excompany@google.com",
            "description" : "Responsible for maintaining the website.",
            "name": "Software Engineer"
        }
        '''
        # check if company exists
        email = request.data.get('email')
        company = Company.objects.filter(email = email)
        if company.exists():
            data = {
                "company": company[0].id,
                "description": request.data.get('description'),
                "name": request.data.get('name')
            }
            serializer = CompanyJobSerializer(data=data)
            # duplicate job allowed here
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                # invalid serializer
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error' : 'Company does not exist'}, status=status.HTTP_400_BAD_REQUEST)


# GENERAL USER API
class UserApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the users
        '''
        users = User.objects.all().values_list()
        return Response(users, status=status.HTTP_200_OK)

# USER SIGNUP API
class SignUpApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # check if the user exists
        check_user_email = User.objects.filter(email=request.data.get('email'))
        if check_user_email:
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        ''' Create a User '''
        data = {
            'email': request.data.get('email'), 
            'fname': request.data.get('fname'), 
            'lname': request.data.get('lname'),
            'password': request.data.get('password'),
            'gender': request.data.get('gender'),
            'cv': request.data.get('cv'),
        }

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# USER LOGIN API
class LoginApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # check if the user exists
        check_user_email = User.objects.filter(email=request.data.get('email'))
        if check_user_email:
            user = check_user_email.values()[0]
            # check for password
            if user["password"] == request.data.get('password'):
                return Response(user, status=status.HTTP_201_CREATED)

        return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

# JOB APPLY
class ApplyJobApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        check_apply = JobUser.objects.filter(companyJob=request.data.get('companyJob'), user=request.data.get('user'))

        # if not applied
        if not check_apply:
            data = {
                'companyJob': request.data.get('companyJob'), 
                'user': request.data.get('user'),
                'status': 0
            }

            serializer = JobUserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({"result": "User already applied"}, status=status.HTTP_201_CREATED)

# JOB UNAPPLY
class UnapplyJobApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        JobUser.objects.filter(companyJob=request.data.get('companyJob'), user=request.data.get('user')).delete()
        return Response({"result": "User unapplied"}, status=status.HTTP_201_CREATED)

# ADD SKILL
class AddSkillApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = {
            'user': request.data.get('user'),
            'name': request.data.get('name'), 
        }

        serializer = UserSkillSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"result": "User added skill"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# REMOVE SKILL
class RemoveSkillApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        UserSkill.objects.filter(id=user=request.data.get('skill_id')).delete()
        return Response({"result": "User removed skill"}, status=status.HTTP_201_CREATED)

# GET USER SKILL LIST
class UserSkillApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user_skill_list = UserSkill.objects.filter(user=request.data.get('user')).values()
        return Response(user_skill_list, status=status.HTTP_201_CREATED)

# ADD AVAILABLE COMPANY JOB SKILL 
class JobSkillApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the Job skills
        '''
        jobskills = JobSkill.objects.all().values_list()
        return Response(jobskills, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create a Job skill
        POST example
        {
            "companyJob": 1,
            "name": "Python"
        }
        '''
        data = {
            "companyJob": request.data.get('companyJob'),
            "name": request.data.get('name')
        }
        serializer = JobSkillSerializer(data=data)
        if serializer.is_valid():
            # check duplicate 
            if not JobSkill.objects.filter(companyJob = request.data.get('companyJob'), name = request.data.get('name')).exists():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'error' : 'Job skill already exists'}, status=status.HTTP_400_BAD_REQUEST)
        # invalid serializer
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET USER JOB LIST
class JobUserApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user_job_list = JobUser.objects.filter(user=request.data.get('user')).values()
        return Response(user_job_list, status=status.HTTP_201_CREATED)
