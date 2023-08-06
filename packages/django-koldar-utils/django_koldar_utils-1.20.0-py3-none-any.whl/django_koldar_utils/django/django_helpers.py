import enum

import stringcase
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class PermissionClass(enum.Enum):
    """
    An enumeration that list all the possible actions a permission can use
    """
    CREATE = "add"
    READ = "view"
    UPDATE = "change"
    DELETE = "delete"


def get_app_label_of_model(model_type: type) -> str:
    """
    get the app owning the given model

    :param model_type: type of the model whose app we need to obtain
    :see: https://stackoverflow.com/a/47436214/1887602
    """
    obj_content_type = ContentType.objects.get_for_model(model_type, for_concrete_model=False)
    return obj_content_type.app_label


def get_permission_name(action: PermissionClass, model: type, app_label: str = None) -> str:
    """
    Fetch the code name of a permission

    :param action: the action a standard permission should allow
    :param model: model involved
    :param app_label: name of the app where the model belongs to. If missing we will compute it from the meta in the model
    :return: permission code name that can be used in permission_required
    """
    if app_label is None:
        app_label = get_app_label_of_model(model)
    return f"{app_label}.{action.value}_{stringcase.lowercase(model)}"


def get_permission_create_name(model: type, app_label: str = None) -> str:
    """
    Fetch the code name of a create permission

    :param model: model involved
    :param app_label: name of the app where the model belongs to. If missing we will compute it from the meta in the model
    :return: permission code name that can be used in permission_required
    """
    return get_permission_name(PermissionClass.CREATE, model, app_label)


def get_permission_read_name(model: type, app_label: str = None) -> str:
    """
    Fetch the code name of a read permission

    :param model: model involved
    :param app_label: name of the app where the model belongs to. If missing we will compute it from the meta in the model
    :return: permission code name that can be used in permission_required
    """
    return get_permission_name(PermissionClass.READ, model, app_label)


def get_permission_update_name(model: type, app_label: str = None) -> str:
    """
    Fetch the code name of an update permission

    :param model: model involved
    :param app_label: name of the app where the model belongs to. If missing we will compute it from the meta in the model
    :return: permission code name that can be used in permission_required
    """
    return get_permission_name(PermissionClass.UPDATE, model, app_label)


def get_permission_delete_name(model: type, app_label: str = None) -> str:
    """
    Fetch the code name of a delete permission

    :param model: model involved
    :param app_label: name of the app where the model belongs to. If missing we will compute it from the meta in the model
    :return: permission code name that can be used in permission_required
    """
    return get_permission_name(PermissionClass.DELETE, model, app_label)

