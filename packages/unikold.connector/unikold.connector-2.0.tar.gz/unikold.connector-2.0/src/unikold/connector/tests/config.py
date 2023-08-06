# -*- coding: utf-8 -*-
soap_test_url = u'http://webservices.daehosting.com/services/isbnservice.wso?WSDL'
soap_test_method = u'IsValidISBN13'
soap_test_method_parameter = u'9783492700764'

xml_test_url = u'https://en.wikipedia.org/w/api.php?format=xml&action=query&prop=extracts&exintro&explaintext&redirects=1&titles=Rick_and_Morty'  # noqa: E501

xml_basic_auth_url = u'https://www.rlp-forschung.de/public/people/Dietrich_Paulus.xml'  # noqa: E501
xml_basic_auth_username = u'mbarde'
xml_basic_auth_password = u'VB*147!abs'

# config data needed for LSF tests
lsf_wsdl_url = u'https://klips.uni-koblenz.de/qisserver/services/dbinterface?WSDL'
lsf_test_object_type = u'Lecture'  # LSF object type
lsf_test_conditions = [('id', '110903'), ('_Bezugssemester', '20182')]
lsf_auth_test_object_type = u'KOLAPerson'
lsf_auth_test_conditions = [('mail', 'mbarde@uni-koblenz.de')]
lsf_wsdl_search_url = u'https://klips.uni-koblenz.de/qisserver/services/soapsearch?WSDL'
lsf_search_test_method_parameter = b'<search><object>person</object><expression><column name="personal.nachname" value="Barde" /><column name="personal.vorname" value="Matthias" /></expression></search>'  # noqa: E501
lsf_auth_username = u'soapadmin'
lsf_auth_password = u'1q2w3e$r'

ldap_server_address = u'ldap://ldap.uni-koblenz.de'
ldap_server_port = 389
ldap_server_base_dn = u'dc=uni-koblenz-landau,dc=de'
ldap_search_username = u'uid=test01,ou=people,ou=koblenz,dc=uni-koblenz-landau,dc=de'
ldap_search_password = u'VB*147!abs'
