from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Course
from .serializers import CourseSerializer
from rest_framework import viewsets
from rest_framework.decorators import action

from .models import Student, Enrollment
from .serializers import (
    StudentSerializer,
    EnrollmentSerializer
)


class CourseListView(APIView):

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CourseDetailView(APIView):

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None

    def get(self, request, pk):
        course = self.get_object(pk)

        if not course:
            return Response(status=404)

        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, pk):
        course = self.get_object(pk)

        if not course:
            return Response(status=404)

        serializer = CourseSerializer(
            course,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=400
        )

    def delete(self, request, pk):
        course = self.get_object(pk)

        if not course:
            return Response(status=404)

        course.delete()
        return Response(status=204)
    
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):

        course = self.get_object()

        enrollments = Enrollment.objects.filter(
            course=course
        )

        students = [
            enrollment.student
            for enrollment in enrollments
        ]

        serializer = StudentSerializer(
            students,
            many=True
        )

        return Response(serializer.data)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer