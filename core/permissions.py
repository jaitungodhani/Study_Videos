from django.contrib.auth.models import Group
from rest_framework import permissions


def _is_in_group(user, group_name):
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None

def _has_group_permission(user, required_groups):
    return any([_is_in_group(user,group_name) for group_name in required_groups])


class IsAdmin(permissions.BasePermission):
    required_groups = ["Admin"]

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission


class IsFaculty(permissions.BasePermission):
    required_groups = ["Faculty"]

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission

class IsSubscribedFaculty(permissions.BasePermission):
    required_groups = ["Subscribed Faculty"]

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission
    
class IsStudent(permissions.BasePermission):
    required_groups = ["Student"]

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission

class IsSubscribedStudent(permissions.BasePermission):
    required_groups = ["Subscribed Student"]

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission
    

class IsUserItSelf(permissions.BasePermission):

    message = 'You must be the creator of this object.'

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj.id == request.user.id
    
class IsUserItSelfforVideos(permissions.BasePermission):

    message = 'You must be the creator of this object.'

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj.for_channel.created_by.id == request.user.id
    
class IsUserItSelfforVideosChannel(permissions.BasePermission):

    message = 'You must be the creator of this object.'

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj.created_by.id == request.user.id
    
class IsUserItSelfforVideosFileUpload(permissions.BasePermission):

    message = 'You must be the creator of this object.'

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj.uploaded_by.id == request.user.id
    
class IsUserItSelfforThumnails(permissions.BasePermission):

    message = 'You must be the creator of this object.'

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        return obj.video_file.uploaded_by.id == request.user.id