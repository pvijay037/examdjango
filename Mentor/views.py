from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Mentor, Student
from .serializers import MentorSerializer, StudentSerializer

class MentorViewSet(viewsets.ModelViewSet):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer

    @action(detail=True, methods=['post'])
    def add_student(self, request, pk=None):
        mentor = self.get_object()
        student_email = request.data.get('student_email')
        if not student_email:
            return Response({'error': 'Please provide a student email'}, status=400)

        student, created = Student.objects.get_or_create(email=student_email, mentor=mentor)
        return Response({'student_id': student.id, 'message': 'Student added successfully'}, status=201)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
