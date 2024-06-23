from django.utils.translation import activate
from django.http import HttpResponseRedirect

class ModifyDefaultLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 获取浏览器的语言首选项
        user_language = request.headers.get('Accept-Language', 'en')
        # Get the previous URL from the HTTP_REFERER header
        # previous_url = request.META.get('HTTP_REFERER', '/')
        # print(previous_url)
        # print(type(previous_url))

        activate(user_language)
        # print("default language")
        # print(user_language)

        if request.method == 'POST':
            # print("language in")
            language = request.POST.get('language')
            if language:
                # print("language~~",language)
                response = HttpResponseRedirect('/')
                # response = HttpResponseRedirect(previous_url)
                # response = HttpResponseRedirect(request.POST.get('next', '/'))
                response.set_cookie('django_language', language)
                activate(language)
                return response

        response = self.get_response(request)
        return response
    

