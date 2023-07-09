from .models import UserGroup, CustomUser

def resetGroups():
    # for grade in CustomUser.grade_list:
    #     UserGroup.objects.create(
    #         category=2,
    #         number=grade[0],
    #         name=grade[1]
    #     )
    for user in CustomUser.objects.all():
        user.group.add(UserGroup.objects.get(category=3, number=0))
    