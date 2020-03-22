from django.db import models

# Create your models here.
class automodel(models.Model):
    auto_type = models.CharField(max_length = 20)#表格操作类别excel word
    func = models.CharField(max_length = 50)#功能
    desc = models.TextField()#功能简述
    auther = models.CharField(max_length= 20)#作者
    remarks = models.CharField(max_length = 30)#备注
    #created = models.DateTimeField(auto_now_add=True)

    #class Meta:
    #   ordering = ('-created',)

    def __str__(self):
        return self.func


# from autoexcel.models import automodel
# automodel.objects.create(pk = 3,auto_type='excel',func = '表格内sheet拆分',desc = '将单个表格中多个sheet页拆分为多个表格')
