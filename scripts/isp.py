#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from http://listingsca.com/computing/internet/providers/#
ISPS = {
    'AOL Canada': {
        'url': 'http://www.aol.ca/',
        },
    'AT&T Canada': {
        'url': 'http://www.att.com/canada/',
        },
    'AT&T Canada Internet and E-Business Services': {
        'url': 'http://www.allstream.com/',
        },
    'Bell Canada': {
        'url': 'http://www.bell.ca/',
        },
    'Canadian Association of Internet Providers': {
        'url': 'http://www.caip.ca/',
        },
    'Rackforce': {
        'url': 'http://www.rackforce.com/',
        },
    'Dialup At Cost': {
        'url': 'http://www.dialupatcost.ca/',
        },
    'FollowMe Canada': {
        'url': 'http://www.followme.com/',
        },
    'ISP.ca': {
        'url': 'http://www.isp.ca/',
        },
    'Lycos Sympatico': {
        'url': 'http://www.sympatico.ca/',
        },
    'Netrover Inc.': {
        'url': 'http://www.netrover.com/',
        },
    'NetZero': {
        'url': 'http://www.netzero.net/',
        },
    'Primus Telecommunications Canada': {
        'url': 'http://www.primus.ca/',
        },
    'SmokeSignal': {
        'url': 'http://www.smokesignal.net/',
        },
    'Sprint Canada': {
        'url': 'http://www.rogerstelecom.ca/',
        },
    'TELUS Internet Services': {
        'url': 'http://www.telus.net/',
        },
    'Thunderstar Internet Access': {
        'url': 'http://www.thunderstar.net/',
        },
    'UNIServe Online': {
        'url': 'http://www.uniserve.com/',
        },
    'Virgin Technologies Inc': {
        'url': 'http://www.virgintechnologies.com/',
        },
}

template = (
"""define host {
       # not working yet, bug reported on Shinken:
       # https://github.com/naparuba/shinken/issues/1218#issuecomment-46223079
       use                      generic-host
       host_name                %(domain)s
       address                  %(domain)s
       alias                    %(domain)s
       check_command            check_dummy!0!OK
}
define service {
       use                      generic-service
       host_name                %(domain)s
       check_command            check_http_service!%(domain)s!%(path)s%(more_options)s
       display_name             %(isp)s
       service_description      %(domain)s
       servicegroups            group-isp
       notes                    order_%(order)d

}
""")

business_rule = (
"""
define host {
       use                            generic-host
       host_name                      ISP
       alias                          ISP
       check_command                  check_dummy!0!OK
}
define service {
       use                            generic-service
       host_name                      ISP
       servicegroups                  group-isp
       service_description            ISP
       # check_command                  bp_rule!g:group_banks
       check_command                  bp_rule!%(all_isp)s
       business_rule_output_template  $(x)$
       notes                          order_0
       icon_image                     fa-signal
}
""")

def main():
    all_isp = []
    for order, (isp, values) in enumerate(ISPS.iteritems()):
        protocol, address = values['url'].split('://')
        domain, path = address.split('/', 1)
        path = '/' + path
        all_isp.append('%s,%s' % (domain, domain))
        
        print template % {'isp': isp,
                         'domain': domain,
                         'path': path,
                         'order': order + 1,
                         'more_options': '!--ssl' if protocol == 'https' else ''}
    all_isp = '&'.join(all_isp)
    print business_rule % {'all_isp': all_isp}

if __name__ == '__main__':
    main()
