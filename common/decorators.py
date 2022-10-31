from django.http import HttpResponseBadRequest

def ajax_required(f):
    """必须是ajax请求,否则返回错误404"""
    def wrap(request,*args,**kwargs):
        if not request.is_ajax():
            # 不是ajax请求，返回错误
            return HttpResponseBadRequest()
        # 是ajax请求则返回本身
        return f(request, *args, **kwargs)
    # 回复原有函数的内容
    wrap.__doc__=f.__doc__
    wrap.__name__=wrap.__name__
    return wrap