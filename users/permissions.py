from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Проверка на вхождение в группу модераторов
    """

    message = "Пользователь не является модератором"

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()

class IsNotModerator(permissions.BasePermission):
    """
    Проверка, что пользователь НЕ входит в группу «moderators»
    """
    message = "Доступ запрещён: вы являетесь модератором"

    def has_permission(self, request, view):
        # Возвращаем True, если пользователь НЕ в группе "moderators"
        return not request.user.groups.filter(name="moderators").exists()

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class IsOwner(permissions.BasePermission):
    """
    Проверка на пользователя-владельца
    """

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
