

#How to scrape a website that requires login with Python


#We will perform the following steps:

#Extract the details that we need for the login
#Perform login to the site
#Scrape the required data

#Step 1: Study the website
#Open the login page

# 1 - Right click on the “Username or email” field and select “inspect element”. 
#We will use the value of the “name” attribue for this input which is “username”. 
#“username” will be the key and our user name / email will be the value 
#(on other sites this might be “email”, “user_name”, “login”, etc.)

# 2 - Right click on the “Password” field and select “inspect element”. 
#In the script we will need to use the value of the “name” attribue for this input which is “password”. 
#“password” will be the key in the dictionary and our password will be the value 
#(on other sites this might be “user_password”, “login_password”, “pwd”, etc.). 

# 3 - In the page source, search for a hidden input tag called “csrfmiddlewaretoken”. 
#“csrfmiddlewaretoken” will be the key and value will be the hidden input value 
#(on other sites this might be a hidden input with the name “csrf_token”, “authentication_token”, etc.). For example “Vy00PE3Ra6aISwKBrPn72SFml00IcUV8”.


#We will end up with a dict that will look like this:
payload = {
        "username": "wpessoa", 
        "password": "Lucidalba210", 
        "csrfmiddlewaretoken": "MUJqngly4mnAOgNeL5yG2pfJqPOZV6y9" #QpOWOxyPsDYkJaSIzCwQ9bjF5vE0x5Tz ou ihEosY6OF4jiAEtw1qwVVaHlPMsVz1jo
}



#Step 2: Perform login to the site
#For this script we will only need to import the following:

import requests  #biblioteca para abrir a URL, pegar o seu conteúdo etc
from lxml import html


#Step 2: Perform login to the site
#First, we would like to create our session object. 
#This object will allow us to persist the login session across all our requests.

session_requests = requests.session()


#Step 2: Perform login to the site
#Second, we would like to extract the csrf token from the web page, this token is used during login. 
#For this example we are using lxml and xpath, we could have used regular expression or any other method 
#that will extract this data. 

login_url = "http://www.intranet.cni.org.br/login/?next=/"
result = session_requests.get(login_url)

tree = html.fromstring(result.text)
authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]

#** More about xpath and lxml can be found here =>>  http://lxml.de/xpathxslt.html



#Next, we would like to perform the login phase. In this phase, we send a POST request to the login url. 
#We use the payload that we created in the previous step as the data. 
#We also use a header for the request and add a referer key to it for the same url.

result = session_requests.post(
        login_url, 
        data = payload, 
        headers = dict(referer=login_url)
)

#Step 3: Scrape content
#Now, that we were able to successfully login, we will perform the actual scraping from CNI INTRANET

url = 'http://www.intranet.cni.org.br/'
result = session_requests.get(
        url, 
        headers = dict(referer = url)
)



#Step 3: Scrape content
#In order to test this, let’s scrape the list of projects from the bitbucket dashboard page. 
#Again, we will use xpath to find the target elements and print out the results. 
#If everything went OK, the output should be the list of buckets / project that are in your bitbucket account.


tree = html.fromstring(result.content)
teste_names = tree.xpath("//div[@class='wa-contacts']/a/text()")

print(teste_names)


#You can also validate the requests results by checking the returned status code from each request. 
#It won’t always let you know that the login phase was successful but it can be used as an indicator.

#result.ok # Will tell us if the last request was ok
result.status_code # Will give us the status from the last request


# In[2]:


url = 'http://www.intranet.cni.org.br/'
p = requests.get(url)
#file = open('IBGE.txt', 'a')   #incluir ***
#s = bs(p.content, 'lxml')  #aqui é o pulo do gato, eu faço a sopa (parser) do html nos seus componentes
s = bs(p.content, 'html.parser')  #aqui é o pulo do gato, eu faço a sopa (parser) do html nos seus componentes

tabelas = s.findAll('div')  #na sopa peguei todas as div

