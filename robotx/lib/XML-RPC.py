"""
A library for XML-RPC testing.

Author: Xin Gao <fdumpling@gmail.com>
Date:   Feb 21, 2013
"""

import cookielib
import tempfile
import urllib2
import xmlrpclib


class BzRpcLib:

    def __init__(self, baseurl, is_cookie=True):
        self.baseurl = baseurl
        self.is_cookie = is_cookie

    def set_xmlrpc(self):
        """Set xmlrpc server proxy"""
        baseurl = self.baseurl
        is_cookie = self.is_cookie
        rpcurl = baseurl + '/xmlrpc.cgi'
        if is_cookie:
            tmpfile = tempfile.NamedTemporaryFile(prefix=".bzcookie.")
            cookiefile = tmpfile.name
            cj = cookielib.LWPCookieJar(cookiefile)
            transport = CookieTransport(rpcurl, cj)
            xmlrpc = xmlrpclib.ServerProxy(rpcurl, transport)
        else:
            xmlrpc = xmlrpclib.ServerProxy(rpcurl)
        return xmlrpc

    def method_execute(self, method_name, value='',
                       user='test_rhuser@abcd.com', password='abcd'):
        """For method execution"""
        xmlrpc = self.set_xmlrpc()
        user_value = {'login': user, 'password': password}
        xmlrpc.User.login(user_value)
        method = 'xmlrpc.' + method_name + '(' + str(value) + ')'
        try:
            results = eval(method)
        except Exception, fault_info:
            if fault_info.faultCode and fault_info.faultString:
                return str(fault_info.faultCode), fault_info.faultString
            else:
                print "false/error info: ", fault_info
                raise
        else:
            print results
            return results

    def create_user(self, email, password='abcd'):
        """For account create"""
        xmlrpc = self.set_xmlrpc()
        user_value = {'login': 'xgao@abcd.com', 'password': 'abcd'}
        try:
            xmlrpc.User.login(user_value)
            new_user = {'email': email, 'password': password}
            xmlrpc.User.create(new_user)
        except Exception, error_info:
            raise error_info

    def login_with_account(self, email, password='abcd'):
        """For web page login"""


class CookieTransport(xmlrpclib.Transport):
    """For cookie transport instance"""
    def __init__(self, uri, cookiejar, use_datetime=0):
        self.verbose = 0
        # python 2.4 compat
        if hasattr(xmlrpclib.Transport, "__init__"):
            xmlrpclib.Transport.__init__(self, use_datetime=use_datetime)
        self.uri = uri
        self.opener = urllib2.build_opener()
        self.opener.add_handler(urllib2.HTTPCookieProcessor(cookiejar))

    def request(self, host, handler, request_body, verbose=0):
        req = urllib2.Request(self.uri)
        req.add_header('User-Agent', self.user_agent)
        req.add_header('Content-Type', 'text/xml')
        if hasattr(self, 'accept_gzip_encoding') and self.accept_gzip_encoding:
            req.add_header('Accept-Encoding', 'gzip')
        req.add_data(request_body)
        resp = self.opener.open(req)
        # In Python 2, resp is a urllib.addinfourl instance, which does not
        # have the getheader method that parse_response expects.
        if not hasattr(resp, 'getheader'):
            resp.getheader = resp.headers.getheader
        if resp.code == 200:
            self.verbose = verbose
            return self.parse_response(resp)
        resp.close()
        raise xmlrpclib.ProtocolError(self.uri, resp.status,
                                      resp.reason, resp.msg)
