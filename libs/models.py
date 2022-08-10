from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True

    @staticmethod
    def trans_fields(data, mapping, reverse=False):
        r = dict()
        for m in mapping:
            if reverse:
                r[0] = data.get(m[-1])
            else:
                r[-1] = data.get(m[0])
        return r
