# _*_ coding: utf-8 _*_
_author__ = 'Aaron'
__time__ = '2018/5/10'

import django.dispatch

op_log = django.dispatch.Signal(providing_args=["admin", "reason"])


def oplog_save(sender, **kwargs):
    kwargs.pop("signal")
    sender.objects.create(**kwargs)


op_log.connect(oplog_save)
