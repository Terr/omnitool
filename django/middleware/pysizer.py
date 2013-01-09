from django.conf import settings

from sizer import scanner, annotate, formatting


class PysizerCreatorsMiddleware(object):
    """Doesn't work and requires patched version of Python
    (http://pysizer.8325.org/INSTALL).

    Also, need to capture output of formatting.printsizes() and output it to a
    file,
    """
    def process_response(self, request, response):
        if settings.DEBUG:
            if request.GET.has_key('creators'):
                objs = scanner.Objects()
                creators = annotate.findcreators(objs)

                formatting.printsizes(
                    creators.back,
                    count=request.GET.get('num_creators', 10)
                )
        return response


class PysizerTestMiddleware(object):
    def process_view(self, request, *args, **kwargs):
        import debug
