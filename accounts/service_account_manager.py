from django.contrib.contenttypes.models import ContentType
import json

from django.core import serializers


# def get_user_service_accounts(user):
#     data = []
#     for s in user:
#         content_type = ContentType.objects.get_for_model(s.content_type.model_class())
#         res = content_type.get_all_objects_for_this_type(pk=s.object_id)
#         serializer = serializers.serialize('json', res)
#         res = json.loads(serializer)
#         data.append(res[0])
#     return data
#
#
# def save_user_service_accounts(user, model, pk):
#     new_service_account = UserServiceAccounts.objects.create(
#         user=user,
#         content_type=ContentType.objects.get_for_model(model),
#         object_id=pk, )
#     print(new_service_account)
#     new_service_account.save()
