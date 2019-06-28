from ldap3 import Server, Connection, ALL, NTLM, Tls
import ssl
import requests
import json

domain_user = 'ml\\admin_XXX'
domain_pass = ''
fury_portal_stock_token = ''
country = 'MLU'

possible_countries = ['MCO','MLA','MLB','MLC','MLM','MLP','MLU','MLV']
if (country in possible_countries):
	# LDAP Server and connection configurations
	tls_config = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1)
	server = Server('ldap://us-admeli.name', use_ssl=True, tls=tls_config, get_info=ALL)
	conn = Connection(server, user=domain_user, password=domain_pass, authentication=NTLM)

	# Init Connection
	print('Conectando con AD..')
	conn.bind()
	print('Conexion Exitosa!!..')

	# Search Parameters
	search_filter = '(userAccountControl=514)'
	search_base = 'OU='+country+',OU=Usuarios Finales,OU=Usuarios,OU=MELI,OU=MercadoLibre,DC=ml,DC=com'
	search_atributes = ['sAMAccountName']

	# Make the Search
	conn.search(search_base, search_filter, attributes=search_atributes)
	response = conn.response

	# Snipe server and connection
	headers = {
		'Content-Type': 'application/json',
		'x-auth-token': fury_portal_stock_token}

	retorno = []
	print('procesando...')
	for row in response:
		ad_user = str(row['attributes']['sAMAccountName'])
		#print(ad_user)
		snipe_url = 'https://shield-test.adminml.com/is-api-stock/v1/stock?username=' + ad_user
		stock_response = eval(json.dumps(requests.get(snipe_url, headers=headers).json()))
		#print(stock_response)
		retorno.append({
			"username": ad_user,
			"assets": stock_response,
		})
	print(retorno)
else:
	errorMsg = "No possible value: " + country
	print({"error": errorMsg})