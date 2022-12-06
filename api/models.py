from django.db import models


# 定义用户模型类 UserInfo
class UserInfo(models.Model):
    username = models.CharField(max_length=16, verbose_name='姓名')
    password = models.CharField(max_length=32, verbose_name='密码')
    certification = models.BooleanField(default=False, verbose_name="是否认证")
    is_delete = models.BooleanField(default=False, verbose_name="逻辑删除")

    class Meta:
        db_table = "402_users"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class UserDetailInfo(models.Model):
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE, verbose_name="关联外键")
    phone = models.CharField(max_length=11, verbose_name='手机号码')
    group = models.CharField(max_length=5, verbose_name='组别')
    job = models.CharField(max_length=5, verbose_name='职务')
    email = models.EmailField(null=True, verbose_name="邮箱")
    is_delete = models.BooleanField(default=False, verbose_name="逻辑删除")

    class Meta:
        db_table = "402_users_details"
        verbose_name = "用户详细信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.group


class RecordsInfo(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name="姓名", related_name="details")
    starttime = models.DateTimeField(verbose_name="开始时间")
    endtime = models.DateTimeField(verbose_name="结束时间")
    choice = models.CharField(max_length=9, verbose_name="会议类型")
    text = models.CharField(max_length=200, null=True, verbose_name="补充说明信息")
    is_delete = models.BooleanField(default=False, verbose_name="逻辑删除")

    class Meta:
        db_table = "402_user_records"
        verbose_name = "预约记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.choice


class KeyInfo(models.Model):
    where_is_key = models.CharField(max_length=200, null=True, verbose_name="钥匙在哪儿")

    class Meta:
        db_table = "where_is_key"
        verbose_name = "钥匙在哪儿"
        verbose_name_plural = "钥匙在哪儿"

    def __str__(self):
        return self.where_is_key
