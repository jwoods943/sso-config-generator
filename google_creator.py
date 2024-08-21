#NO AUTHORIZDATION AVILABLE FOR GOOGLE

#well known discovery is the same

#function for customer to enter their audience

#function to set client id, this is the same value as audience.

#function for customer to enter username claim

#function for customer to enter client_secret
import re
def main_func(sso_button_text, providers):
    print("test")
    #creates an empty list that will have lines of config appended
    config_list = []
    #calls set_client_id and sets the client_id variable to its return value
    client_id = set_client_id()
    #calls set_client_secret and assigns the return value to variable client_secret
    client_secret = set_client_secret()
    #for the google idp the audience is the same as the client id so we can set audience = client_id
    audience = client_id
    #sets user_principal variable to email, this is rarely changed for google auth SSO so this is hardcoded
    user_principal = "email"
    
    #join the providers into a single string separated by a comma, it is necessary to define the separator as a string as below
    #appends both the joint authorization and authentication providers to the config list - this is duplicated code and should be refactored
    separator = ","
    joint_authentication_providers = separator.join(providers["authentication"])
    joint_authorization_providers = separator.join(providers["authorization"])
    config_list.append(f"dbms.security.authentication_providers={joint_authentication_providers}")
    config_list.append(f"dbms.security.authorization_providers={joint_authorization_providers}")
    
    #sets the well_known_discovery_URI to https://accounts.google.com/.well-known/openid-configuration, this is always the same for google auth
    well_known_discovery_uri = "https://accounts.google.com/.well-known/openid-configuration"
    
    #generates parameter for the sso button text, using the sso_button_text parameter and appends to config_list    
    config_list.append(f"dbms.security.oidc.google.display_name={sso_button_text}")
    
    #generates the parameter for the well known discovery uri based on teh well_known_discovery_uri variable and appends to config_list
    config_list.append(f"dbms.security.oidc.google.well_known_discovery_uri={well_known_discovery_uri}")
    
    #generates the auth_flow parameter, no user input handles, this line is always the same
    config_list.append("dbms.security.oidc.google.auth_flow=pkce")
    
    #hardcoded email principal, and id token type in the config map and appends the parameter to the config_list
    config_list.append(f"dbms.security.oidc.google.config=principal=email;code_challenge_method=S256;token_type_principal=id_token;token_type_authentication=id_token")
    
    #generates the audience parameter and appends to the config list based on the audience variable
    config_list.append(f"dbms.security.oidc.google.audience={audience}")
    
    #appends the scopes parameter to the config list, this includes the google email and profile scopes, nothing else should be needed so this is hardcoded
    config_list.append(f"dbms.security.oidc.google.params=client_id={client_id};response_type=code;access_type=offline;scope=openid profile email https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email")
    
    #appends the token endpoint parameter to the config list, this is always the same for google auth
    config_list.append(f"dbms.security.oidc.google.token_endpoint=https://oauth2.googleapis.com/token")
    
    #appends the auth endpoint parameter to the config list, this is always the same for google auth
    config_list.append(f"dbms.security.oidc.google.auth_endpoint=https://accounts.google.com/o/oauth2/v2/auth")
    
    #appends the client secret parameter to the config
    config_list.append(f"dbms.security.oidc.google.token_params=client_secret={client_secret}")
    
    #writes the config_list to a file
    with open('sso_config_test.txt', 'w+') as file:
        for parameter in config_list:
            file.write(f"{parameter}\n")

    
#function that accepts user input, calls another function to validate the input
def set_client_id():
    #promps user to enter their client id 
    client_id  = input("Please enter your Google Client ID, for example: 729287977690-d1kmti260aebur3bl06vag30i49vogi5.apps.googleusercontent.com")
    return client_id

def set_client_secret():

    #prompts user to enter their client secret
    client_secret = input("Please enter client secret:")
    return client_secret
    
        
            

