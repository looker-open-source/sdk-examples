## Sample iOS Swift SDK Example

### Setting the Looker Instance URL

To set the looker instance URL go to the app delegate line 17 and set
config.base_url to the url for the looker api you will be using. For
example:

https://foo.looker.com:19999


### Setting client_id and client_secret

There are a couple different ways to pass the client_id and 
client_secret to the sdk. This example sets them as environment vars. 
To set the environment vars go to `Product`>`Scheme`>`Edit Scheme...` 
and add

- LOOKERSDK_CLIENT_ID
- LOOKERSDK_CLIENT_SECRET
