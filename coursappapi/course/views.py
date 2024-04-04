from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action
from course.models import Category, Lesson, Course, User, Comment, Like
from rest_framework.response import Response
from course import serializers, paginator, perms


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

    # page = self.paginate_queryset(queryset)
    # if page is not None:
    #     serializer = self.get_serializer(page, many=True)
    #     return self.get_paginated_response(serializer.data)
    #
    # serializer = self.get_serializer(queryset, many=True)
    # return Response(serializer.data)

    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):

        paginators = paginator.CommentPaginator()
        comment = self.get_object().comment_set.select_related('user').order_by("-id")
        page = paginators.paginate_queryset(comment, request)

        if page is not None:
            serializer = serializers.CommentSerializer(page, many=True)
            return paginators.get_paginated_response(serializer.data)

        return Response(serializers.CommentSerializer(comment, many=True).data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ["current_user"]:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self, request, pk):
        comments = self.get_object().comment_set.create(content=request.data.get('content'), user=request.user)

        return Response(serializers.CommentSerializer(comments, many=True).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        li, created = Like.objects.get_or_create(lesson=self.get_object(), user=request.user)

        if not created:
            li.active = not li.active
            li.save()

        return Response(serializers.LessonDetailSerializer(self.get_object()).data, status=status.HTTP_200_OK)



class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action in ["current_user"]:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=["get", "patch"], url_path="current_user", detail=False)
    def get_current_user(self, request):
        user = request.user
        if request.method.__eq__('PATCH'):
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()

        return Response(serializers.UserSerializer(request.user).data)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [perms.CreateOwner]





