import re
import requests

#function to set groups claim, leave blank if no group mapping required

#function to set username claim

#function to configure group to role mapping, caution - quotes are required




### user prompts:
# Application (Client ID)
# Directory (Tenant ID)
# API URI

# called by the sso_config_tool.py file to generate the config for an azure instance
# takes the token type, providers and sso_button_text parameters
def main_func(token_type, providers, sso_button_text):
    config_list = []
    client_id = set_client_id()
    audience = set_audience(client_id, token_type)
    user_principal = set_user_principal()
    tenant_id = set_tenant_id()
    well_known_discovery_uri = set_well_known_discovery_uri(tenant_id)
    scopes = set_scopes(client_id, token_type)
    
    #join the providers into a single string separated by a comma, it is necessary to define the separator as a string as below
    #appends both the joint authorization and authentication providers to the config list
    separator = ","
    joint_authentication_providers = separator.join(providers["authentication"])
    joint_authorization_providers = separator.join(providers["authorization"])
    config_list.append(f"dbms.security.authentication_providers={joint_authentication_providers}")
    config_list.append(f"dbms.security.authorization_providers={joint_authorization_providers}")
    
    #generates parameter for the sso button text, using the sso_button_text parameter and appends to config_list    
    config_list.append(f"dbms.security.oidc.azure.display_name={sso_button_text}")
    
    #generates the parameter for the well known discovery uri based on teh well_known_discovery_uri variable and appends to config_list
    config_list.append(f"dbms.security.oidc.azure.well_known_discovery_uri={well_known_discovery_uri}")
    
    #generates the auth_flow parameter, no user input handles, this line is always the same
    config_list.append("dbms.security.oidc.azure.auth_flow=pkce")
    
    #sets token_type_config to the relevant string based on the selected token type for further use
    match token_type:
        case "ID Token":
            token_type_config = "id_token"
        case "Access Token":
            token_type_config = "access_token"
    #generates the config map using token type and user principal to the config_list
    config_list.append(f"dbms.security.oidc.azure.config=principal={user_principal};code_challenge_method=S256;token_type_principal={token_type_config};token_type_authentication={token_type_config}")
    
    #generates the issuer based on the the tenant_id variable, if the token_type is access token
    if token_type == "Access Token":
        config_list.append(f"dbms.security.oidc.azure.issuer=https://sts.windows.net/{tenant_id}/")
    
    #generates the audience parameter and appends to the config list based on the audience variable
    config_list.append(f"dbms.security.oidc.azure.audience={audience}")
    
    
    #creates a string of scope separator by spaces using the scopes variable, with the separator set to space
    separator = " "
    separated_scopes = separator.join(scopes)
    #generates the params parameter and appends to config_list, uses client_id and separated_scopes variables
    config_list.append(f"dbms.security.oidc.azure.params=client_id={client_id};response_type=code;scope={separated_scopes}")
    
    #generates the token endpoint parameter using the tenant id variable
    config_list.append(f"dbms.security.oidc.azure.token_endpoint=https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token")
    
    #generates the auth endpoint parameter using the tenant id variable
    config_list.append(f"dbms.security.oidc.azure.auth_endpoint=https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize")
    
    #writes the config_list to a file
    with open('sso_config_test.txt', 'w+') as file:
        for parameter in config_list:
            file.write(f"{parameter}\n")
            
            
#def set_group_mapping():
#    input(
    

    
#function that asks user for client Id and returns value to the main function
def set_client_id():
    while True:
        #prompts user to enter client id
        client_id = input("""Please enter the Client ID of your azure application:\n""")
        #passes the entered id into the check_for_valid_guid function to validate the input
        valid_guid = check_for_valid_guid(client_id)
        if valid_guid:
            print(f"Client ID set to: {client_id}")
            return client_id
        if not valid_guid:
            print(f"""client_id: {client_id} is not a valid guid for the Azure IDP, please enter a valid guid.\nexample: 4376dc8b-b5af-424f-9ada-c1c1b2d416b9""")

#take the client ID and returns it as it was if the token type is access token, but prepends api:// if access token is being used
def set_audience(client_id, token_type):
    #performs different action depending on token type
    match token_type:
        #for id token, will return the client id as it was
        case "ID Token":
            audience = client_id
        # for access token will prepend api:// to the client id
        case "Access Token":
            audience = "api://" + client_id
    #returns the audience value back to the main function
    return audience
      
#function to set the user principal      
def set_user_principal():
    # While True to loop the function indefinitely, this will loop the function if an invalid option is entered
    while True:
        #displays a selection of commonly used user principals, but allows for a custom option in case it is needed
        selection = input("""Please select the user principal by entering the corresponding number:
        1. sub
        2. upn (Also called User Principal Name)
        3. preferred_username (Please note that this field may not be present, if customer cannot log in, please check for this field in their token
        4. unique_name
        5. email
        6. custom (customers may have their own custom fields, this option allows you to enter free text\n""")
        #returns the relevant string depending on the user selection
    
        match selection:
            case "1":
            	return "sub"
            case "2":
                return "upn"
            case "3":
                return "preferred_username"
            case "4":
                return "unique_name"
            case "5":
                return "email"
            case "6":
                custom_principal = input("Please enter your custom user principal and press enter \n")
                return custom_principal
            case other:
                print("Please enter a valid option")

def set_tenant_id():
    while True:
        #Asks user for tenant ID and stores the value in the tenant_id variable
        tenant_id = input("""Please enter your Directory (tenant) ID and press enter: \n""")
        #calls the check for valid guid function which returns a boolean value
        valid_tenant_id = check_for_valid_guid(tenant_id)
        # if tenant ID is valid returns it
        if valid_tenant_id:
            return tenant_id
        # if tenant ID is invalid, tells the user and loops the function
        if not valid_tenant_id:
            print(f"""Tenant Id: {tenant_id} is not a valid guid for the Azure IDP, please enter a valid guid.
            example: 4376dc8b-b5af-424f-9ada-c1c1b2d416b9""")
    return tenant_id

#generates the well known discovery URI based on the tenant ID, accepts the tenant ID as an argument.
def set_well_known_discovery_uri(tenant_id):
    #inserts the tenant_id into the well know uri to create the full uri
    well_known_discovery_uri = f"https://login.microsoftonline.com/{tenant_id}/v2.0/.well-known/openid-configuration"
    #performs a http request to check if the URI is accessible, warns if a 200 is not received, but will continue with the process
    check_availability = requests.get(well_known_discovery_uri)
    # != 200 means the request was unsuccessful, throws a warning
    if check_availability.status_code != 200:
        print(f"Received error code {check_availability.status_code}, your well known discovery URI may be incorrect")
    #200 means it was successful, lets user know its accessible
    if check_availability.status_code == 200:
        print("Status code 200 received, well known uri is accessible")
    
    #returns the well known discovery uri to the main function
    return well_known_discovery_uri


#function that returns the relevant scopes depending on token type
def set_scopes(client_id, token_type):
    #default scopes that are usually always included
    scopes = ["openid", "profile", "email"]
    #if the token type is access token, asks for the configured scope name in the expose API section of IDP
    if token_type == "Access Token":
        scope_name = input(f"""Please enter the scope that has been configured in the 'Expose API' section of the IDP
        you only need to enter the scope name that comes after the GUID, for example:
        api://54e85725-ed2a-49a4-a19e-11c8d29f9a0f/access-token-scope you only need to enter access-token-scope not the full URI \n""")
        #builds the full scope name using the client id and scope name
        full_scope_name = f"api://{client_id}/{scope_name}"
        #shows the user their scope name
        print(f"Your scope name is: {full_scope_name}")
        #appends the new scope name to the list of scopes
        scopes.append(full_scope_name)
    #returns the list of scopes to the main function
    return scopes
    
#function to check if a guid is in a valid format, returns a boolean true or false depending on the result.
#this is used to validate the tenant ID and client ID as these are in the same format, this will also used for Azure Groups
def check_for_valid_guid(guid_string):
    #regex that checks for the guid format, 8 alpha numberic, followed by 3 groups of 4 alphanumeric followed by a group of 12 alphanumeric
    #with each group being separated by -
    #re.match function returns None if there is no match and a match object if there is a match
    is_guid_valid = re.match("[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$", guid_string)
    #if is_guid_valid is not None, it means there was a match, which means the value is valid
    if is_guid_valid is not None:
        is_guide_valid = True
    #if is_guid_valid is None this means the guid is invalid, so it sets is_guid_valid to false
    else:
        is_guid_valid = False
    return is_guid_valid