import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action

def create_action(user, verb, target=None):
    # 检查在最金一分钟是否有任何类似的行动
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id,  # 单下划线 value 参数需要包含 foreign 模型的主键的原始值
                                            verb=verb,
                                            created__gte=last_minute,
                                            )
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct,
                                                 target_id=target.id
                                                 )
    if not similar_actions:
        # 不存在相似的动作
        action = Action(user=user, verb=verb,target=target)
        action.save()
        return True
    return False
