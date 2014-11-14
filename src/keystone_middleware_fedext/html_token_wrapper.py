#  Copyright (c) 2014 INFN - "Istituto Nazionale di Fisica Nucleare" - Italy
#  All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License. 

import six

from keystone.common.config import CONF
from keystone.common import wsgi
from keystone.openstack.common import log

LOG = log.getLogger(__name__)

#
# TODO missing auto-post
#
html_template = '''<html>
  <head>
    <meta content='text/html; charset=utf-8' http-equiv='Content-Type' />
    <title>Redirect for %(user)s</title>
  </head>
  <body>
    <form method="POST" action="%(url)s">
      <p>
         <label>Token</label>
         <textarea rows="10" cols="80" name="token">%(token)s</textarea>
      </p>
      <p><input type="submit">Send</input></p>
    </form>
  </body>
</html>
'''

class TokenWrapperMiddleware(wsgi.Middleware):

    def __init__(self, *args, **kwargs):
        super(TokenWrapperMiddleware, self).__init__(*args, **kwargs)

    def process_response(self, request, response):
        querystr = dict(six.iteritems(request.params))
        if 'return' in querystr:
            res_headers = dict(six.iteritems(response.headers))
                            
            LOG.info(response.body)

            if 'X-Subject-Token' in res_headers:
                
                response.content_type = 'text/html'
                response.charset = 'UTF-8'
                response.text = html_template % {
                    'url' : querystr['return'], 
                    'token' : res_headers['X-Subject-Token'],
                    'user' : request.environ.get('eppn', 'Unknown')
                }
                
            else:
                LOG.error('Cannot find token in response')

        return response
