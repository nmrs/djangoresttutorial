from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from snippets.serializers import SnippetSerializer
from snippets.serializers import UserSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

class SnippetList(generics.ListCreateAPIView):
    model = Snippet
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def pre_save(self, obj):
    	obj.owner = self.request.user

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Snippet
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

    def pre_save(self, obj):
    	obj.owner = self.request.user

class SnippetHighlight(generics.SingleObjectAPIView):
	model = Snippet
	renderer_classes = (renderers.StaticHTMLRenderer,)

	def get(self, request, *args, **kwargs):
		snippet = self.get_object()
		return Response(snippet.highlighted)

class UserList(generics.ListAPIView):
	model = User
	serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
	model = User
	serializer_class = UserSerializer
