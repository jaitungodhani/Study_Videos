from django.contrib.auth.models import Group


class GroupPermission:
    """
    Group Permission Management
    """

    def __init__(self, user, groups):
        if isinstance(groups, str):
            groups = [groups]

        self.user = user
        self.groups = groups

    def _has_group_permission(self):
        return any([self._is_in_group(group) for group in self.groups])

    def _is_in_group(self, group):
        try:
            return Group.objects.get(
                name=group
            ).user_set.filter(
                id=self.user.id
            ).exists()
        except Group.DoesNotExist:
            return None
