# sso-config-generator
The purpose of this tool is to create SSO configs for a selected provider and token type combination for use with a Neo4j database

You will be asked to select your IDP when you run this tool, the information below corresponds to a token type + IDP combination, please follow the one relevant to you

Before proceeding you should have information from the customer, outlined in the playbook.

##Azure supplemental KBA
https://aura.support.neo4j.com/hc/en-us/articles/20575468736147
## Azure ID Token
1. Select whether you want to include native authentication, this is username + password authentication,
2. Select whether you want to include native authorization, this is for granting permissions to a user. All Azure AD implementations have an authorization server, but if customer still wants username and password auth enabled you will
will need native authorization, otherwise those users won't have any permissions applied to them.
3. Enter the text that you would like to be displayed on the SSO Login button, avoid using special characters besides hyphens to be on the safe side, the customer should have provided this
4. Enter the client ID of the azure application and press enter, you will prompted to enter it again if an incorrect format is used
5. Select the user principal, the customer should have told us what this needs to be, option 6 allows you to enter a principal in free text, in case the customer has custom fields they want to use. If the config doesn't work, you should check
if the selected principal exists in the token.
6. Enter the directory (tenant) id, this will also prompt if an invalid format is used.
7. You may see an error code, this means that your well known discovery URI may be incorrect
8. The config will be generated in the same directory as the tool, it will be a .txt file

## Azure Access Token
1. Select whether you want to include native authentication, this is username + password authentication,
2. Select whether you want to include native authorization, this is for granting permissions to a user. All Azure AD implementations have an authorization server, but if customer still wants username and password auth enabled you will
will need native authorization, otherwise those users won't have any permissions applied to them.
3. Enter the text that you would like to be displayed on the SSO Login button, avoid using special characters besides hyphens to be on the safe side, the customer should have provided this
4. Enter the client ID of the azure application and press enter, you will prompted to enter it again if an incorrect format is used
5. Select the user principal, the customer should have told us what this needs to be, option 6 allows you to enter a principal in free text, in case the customer has custom fields they want to use. If the config doesn't work, you should check
if the selected principal exists in the token.
6. Enter the directory (tenant) id, this will also prompt if an invalid format is used.
7. You may see an error code, this means that your well known discovery URI may be incorrect
8. Enter the created scopes name for your access token, this should have been provided by the customer. You only need to enter the name after the forward slash, for example for the
following scope, you only need to enter access-token-scope and not the full URI: api://54e85725-ed2a-49a4-a19e-11c8d29f9a0f/access-token-scope
9. The config will be generated and stored in a .txt file in the same location as the tool.
