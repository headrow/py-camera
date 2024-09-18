# WARNING
**DO NOT USE THIS SCRIPT TO ACCESS OTHER PEOPLE'S CAMERAS, AS THEY LOG YOUR IP AND CAN GET YOU IN TROUBLE**
# Py Camera
Python script that lets you search for IP Cameras with default credentials using Shodan
# How To Use
- Run main.py
- Insert your Shodan API key
- Select one of the options
- Let the script run
# Add An Option
- Open options.json
- Put a comma on the last method
- Add this and change the values:
```
{
    "name": "Option Name",
    "search": "Shodan Search Term",
    "usernames": [
        ""
    ],
    "passwords": [
        ""
    ]
}
```
# Add A Method
Let's say, as an example, you have the url http://1.1.1.1/admin/test.htm with a login prompt
- Open methods.json
- Find what type of method it uses
- Put a comma on the last method
- Put the url in quotation marks and add it to the file
- Remove the "http://1.1.1.1" part from the url, so you only have "/admin/test.htm"
# Requirements:

### Shodan API Key:
- [Read how to get it here](https://developer.shodan.io/api/requirements)
### Python Libraries:
- [requests](https://pypi.org/project/requests/)
- [shodan](https://github.com/achillean/shodan-python)