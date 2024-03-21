from rest_framework import viewsets, generics, status, parsers
from rest_framework.decorators import action
from course.models import Category, Lesson, Course, User
from rest_framework.response import Response
from course import serializers, paginator


class CategoryViewset(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CourseViewset(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = serializers.CourseSerializer
    pagination_class = paginator.CoursePaginator

    def get_queryset(self):
        queryset = self.queryset

        if self.action == 'list':
            q = self.request.query_params.get('q')
            if q:
                queryset = queryset.filter(name__icontains=q)

            cate_id = self.request.query_params.get('category_id')
            if cate_id:
                queryset = queryset.filter(category_id=cate_id)

            return queryset

    @action(methods=['get'], url_path='lessons', detail=True)
    def get_lesson(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True)

        q = request.query_param.get('q')
        if q:
            lessons = lessons.filter(name__icontains=q)

        return Response(serializers.LessonSerializer(lessons, many=True).data, status=status.HTTP_200_OK)


class LessonViewset(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.prefetch_related('tag').filter(active=True)
    serializer_class = serializers.LessonDetailSerializer

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        comment = self.get_object().comment_set.select_related('user').all()

        return Response(serializers.CommentSerializer(comment, many=True).data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser,]
