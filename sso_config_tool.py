from azure_creator import main_func as azure_main_func
from google_creator import main_func as google_main_func
def idp_selector():
    selection = input("""Please select your IDP from the below options by entering the corresponding number and pressing enter:
            1. Azure
            2. Google""")
    match selection:
        case "1":
            idp = "azure"
            return idp
        case "2":
            idp = "google"
            return idp
        case other:
            print("Please select a valid option")
            idp_selector()
            
            
def set_token_type(idp):
    token_type = input("""Please select token type by entering the corresponding number:
    1. ID Token
    2. Access Token\n""")
    #sets token type to a string, for better visiblity in the code as this will be passed to other functions
    match token_type:
        case "1":
            token_type = "ID Token"
        case "2":
            token_type = "Access Token"
        case other:
            #asks user to select a valid token type
            print("Please select a valid token type")
            #calls the set_token_type function to display options and loop until a valid option is selected
            set_token_type()
    #prints the selected token type to the screen.        
    print(f"Token type {token_type} selected")
    return token_type
    
    
#function to ask user what they want their providers to be called
def set_providers(idp):
    #dictionary which holds the providers, uses idp variable, oidc- is required at the start of the provider
    providers = {
        "authentication": [f"oidc-{idp}"],
        "authorization": [f"oidc-{idp}"]}
    # a list of provider types to iterate over to avoid code duplication
    provider_types = ["authentication", "authorization"]
    #loops over provider_types list and asks if native is needed
    for provider_type in provider_types:
        #asks for user input and stores it in a variable for later use
        include_native = input(f"""Would you like to include native {provider_type}? please enter the number corresponding to your answer:
        1. Yes
        2. No\n""")
        #checks user input
        match include_native:
            #if native is needed appends the string "native" to the provider dictionary. Tells user native type has been included
            case "1":
                providers[provider_type].append("native")
                print(f"Native {provider_type} included")
            #if native is not needed does nothing and tells the user native type has not been included
            case "2":
                print(f"Native {provider_type} not included")
    #returns the dictionary of providers to thge main function for further use
    return providers

def set_providers_google():
    #function is specifically for google, we do not support authorization server for google, so only native is included there
    providers = {
        "authentication": [f"oidc-google"],
        "authorization": ["native"]}
    # a list of provider types to iterate over to avoid code duplication

    #asks for user input and stores it in a variable for later use
    include_native = input(f"""Would you like to include native authentication? please enter the number corresponding to your answer:
    1. Yes
    2. No\n""")
    #checks user input
    match include_native:
        #if native is needed appends the string "native" to the provider dictionary. Tells user native type has been included
        case "1":
            providers["authentication"].append("native")
            print("Native authentication included")
        #if native is not needed does nothing and tells the user native type has not been included
        case "2":
            print(f"Native autentication not included")
    #returns the dictionary of providers to thge main function for further use
    return providers
    
    
#function that asks for user input and returns their input as a string
def set_sso_button_text():
    #gets user input
    sso_button_text = input ("""Please enter the text you want to be displayed on the SSO button and press enter.\nPlease do not use special characters other than hyphens (-)""")
    #returns the user input to the main function
    return sso_button_text
    
    
#calls function to let user set their IDP, this is later passed to set_providers to generate the correct providers
idp = idp_selector()
print(idp)
#calls function to set token type, is later passed to the IDP specific functions to create the config
#This is only called if IDP isn't equal to google as google only supports ID Tokens, so we don't need to pass the idp parameter to the google function
if idp != "google":
    token_type = set_token_type(idp)

#calls the regular set_providers if the idp is not google, google doesn't support authorization so a separate function
#is needed to handle that, prefer to keep this one in tact to avoid overcomplicating the code
if idp != "google":
    #calls function to set providers
    providers = set_providers(idp)

#calls the function to set the providers for google if the idp variable is google
if idp == "google":
    providers = set_providers_google()
    
#calls function to set the text that appears on the SSO button
sso_button_text = set_sso_button_text()

#calls the relevant config creator based on the idp selected by the user
match idp:
    case "azure":
        #passes the token type and providers variables to the azure function to create the config.
        azure_main_func(token_type, providers, sso_button_text)
    case "google":
        #passes sso button text to the google auth main func to generate the config
        google_main_func(sso_button_text)