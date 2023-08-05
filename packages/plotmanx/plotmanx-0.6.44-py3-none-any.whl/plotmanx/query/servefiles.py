# !/usr/bin/env python
import os

import tornado.web
from tornado.escape import xhtml_escape
# from tornado.options import define, options

# config options
"""define('port', default=8080, type=int, help='port to run web server on')
define('debug', default=True, help='start app in debug mode')
define('route_to_index', default=False, help='route all requests to index.html')
options.parse_command_line(final=True)

PORT = options.port
DEBUG = options.debug"""

ROUTE_TO_INDEX = True


class DirectoryHandler(tornado.web.StaticFileHandler):
    def validate_absolute_path(self, root, absolute_path):
        if ROUTE_TO_INDEX and self.request.uri != '/' and not '.' in self.request.uri:
            uri = self.request.uri
            if self.request.uri.endswith('/'):
                uri = uri[:-1]

            absolute_path = absolute_path.replace(uri, '/index.html')

        if os.path.isdir(absolute_path):
            index = os.path.join(absolute_path, 'index.html')
            if os.path.isfile(index):
                return index

            return absolute_path

        return super(DirectoryHandler, self).validate_absolute_path(root, absolute_path)

    def get_content_type(self):
        if self.absolute_path.endswith('.vtt'):
            return 'text/vtt'

        if self.absolute_path.endswith('.m3u8'):
            return 'application/vnd.apple.mpegurl'

        content_type = super(DirectoryHandler, self).get_content_type()

        # default to text/html
        if content_type == 'application/octet-stream':
            return 'text/html'

        return content_type

    @classmethod
    def get_content(cls, abspath, start=None, end=None):
        relative_path = abspath.replace(os.getcwd(), '') + '/'

        if os.path.isdir(abspath):
            html = '<html><title>Directory listing for %s</title><body><h2>Directory listing for %s</h2><hr><ul>' % (relative_path, relative_path)
            for filename in os.listdir(abspath):
                force_slash = ''
                full_path = filename
                if os.path.isdir(os.path.join(relative_path, filename)[1:]):
                    full_path = os.path.join(relative_path, filename)
                    force_slash = '/'

                html += '<li><a href="%s%s">%s%s</a>' % (xhtml_escape(full_path), force_slash, xhtml_escape(filename), force_slash)

            return html + '</ul><hr>'

        if os.path.splitext(abspath)[1] == '.md':
            try:
                import codecs
                import markdown
                input_file = codecs.open(abspath, mode='r', encoding='utf-8')
                text = input_file.read()
                return markdown.markdown(text)
            except:
                import traceback
                traceback.print_exc()
                pass

        return super(DirectoryHandler, cls).get_content(abspath, start=start, end=end)
