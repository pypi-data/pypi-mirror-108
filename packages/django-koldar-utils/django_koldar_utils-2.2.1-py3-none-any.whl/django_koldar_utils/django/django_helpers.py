import enum
from typing import Iterable, Tuple

import django_filters
import stringcase
from django.contrib.contenttypes.models import ContentType


def get_app_label_of_model(model_type: type) -> str:
    """
    get the app owning the given model

    :param model_type: type of the model whose app we need to obtain
    :see: https://stackoverflow.com/a/47436214/1887602
    """
    obj_content_type = ContentType.objects.get_for_model(model_type, for_concrete_model=False)
    return obj_content_type.app_label


def get_name_of_primary_key(model_type: type) -> str:
    """
    Fetch the name of the primary key used in a model

    :param model_type: type of the django model (models.Model) which key you want to fetch
    :return: the name of its primary key
    """
    return model_type._meta.pk.name




