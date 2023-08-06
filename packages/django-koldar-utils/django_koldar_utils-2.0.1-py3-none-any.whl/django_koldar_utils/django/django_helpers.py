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




