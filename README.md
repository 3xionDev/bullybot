# bullybot
lil python script for reminding project partners to finish their portion

---
# Setup
the script should be run inside of its own directory, to ensure that it doesn't confuse other json files with the intended one.

when first run, the script will prompt the user to enter their Gemini API key and Gmail app password. these credentials will then be serialized into JSON and stored in a file named "credentials.json." directions for creating these two essential elements are provided in the script itself. **never** use your own personal email address for the bot. due to this being a bot script, there's always a nonzero chance that google will notice and ban you.

#### WARNING: the way this bot stores your API keys and application passwords *during runtime* is *NOT SECURE.* it caches them in environment variables, meaning that a malicious program can snipe them from right under your nose while the program is running. if this doesn't concern you, run it at your own risk. running the bot inside of an internet-enabled virtual machine (VirtualBox loaded with fedora workstation or something similar) for an added layer of sandboxing and security is what i would recommend.

# Usage
once credentials.json exists, the script will run normally. you'll be prompted for your partner's name and their responsibility in the project. you'll then be asked to tell it how aggressive the message should be and how long the message should be. finally, you'll have to enter your partner's email address. once you've done all of this, the rest is automatic. the script will contact Gemini and prompt it for a message to your partner, and, once it gets a response, it will open a connection to Gmail's SMTP API and attempt to send this message to your partner. if all goes well, your partner will recieve the email within five minutes of the script sending it.

unfortunately, not everything works 100% of the time.

# Troubleshooting
there are a couple things that can go wrong when running the bot.
## Gemini issues
google gemini is really janky and doesn't work about 40% of the time. i would have used chatgpt, but their api is complicated and i didn't really feel like using it. 

### Resource Unavailable / Model Overload
this is the most common type of error, and it occurs when the gemini model being prompted is currently overloaded with requests. i don't know the exact reason for it occurring so much, but my best guess is that google sucks at resource management and they haven't allocated enough resources to the model we're trying to use. this usually happens when google is testing new features, in which case the resources are reallocated to the experimental models. there's no foolproof fix for this error, but what works for me is changing the model being prompted in `credentials.json`. i usually change `"target-gemini-model"` from `"gemini-2.0-flash-lite"` to `"gemini-2.0-flash-exp"` or `"gemini-2.0-flash"`. you can use any text-output model provided by gemini api, but keep in mind that different models have different rate limits.

### Too Many Requests
this is the standard error thrown when you've exceeded any of the rate limits for the model you're using. `gemini-2.0-flash-lite` has a rate limit of 30 requests per minute, so you probably won't encounter this error in normal operation. there's no physically possible way to send a request every 2 seconds without modifying the script. if, somehow, you do run into this error, switching to a different model using the method above should fix it.

### Any network error / Script becomes unresponsive after entering email
when a network issue arises, there are two failure modes that the script may encounter. it may throw a network error such as `HTTP 404`, or the script may become entirely unresponsive after sending the request to gemini. technically, a script freeze doesn't always mean a network error, but that is generally the case, because the script is asynchronous and will simply pause execution if it doesn't receive a response from the api. check whether you're connected to a network, and, if you are, chances are that google gemini is blocked by your network administrator. you can check if this is the case by visiting https://gemini.google.com/ and, if it doesn't load, that's the reason the script is broken. to fix this, you must connect to a different network, otherwise the bot will not work.

there's a rare chance that gemini's api itself will be down. if that's the case, the script will throw a network error such as 404 Not Found. wait a while for the api to come back up, and then try again.

## Gmail issues
TBD. i've never encountered an issue with SMTP, but if i do i'll catalogue it here.

## Script issues
i've also never encountered an error directly involving script execution, but i can think of a few possible failure conditions.
### Any error pertaining to credentials.json
there are a few possible failure conditions involving `credentials.json`. 

if the file is manually edited, changing the name of a key in the json object will result in the script throwing an error. you should be able to fix this by deleting the file and then regenerating it using the script.

if the credentials.json file, for some reason, already exists in the directory the script is stored in, it will not be able to generate its own json file on the first execution. it will attempt to read the json object into a python variable, then will throw an error when it can't find the key:value pairs it expects. to fix this, make sure to put the script **in its own directory,** then run it to regenerate the credentials file. this will ensure that credentials.json is unique to the script's execution.

### Module errors
the script requires a few packages to run. if these modules are not installed, the script will not work. the following packages are required (python 3.13 and above required):
`google-genai`
`smtplib`

to install these, you can run `pip install -q -U google-genai` and `pip install smtplib`. i recommend using PyCharm IDE because it simplifies dependencies and package management, and is generally just a good IDE.

# Credit
the script is written entirely by me, but i pulled heavily off of stackoverflow to get smtp working. other contributions were done by https://github.com/confusedgmcst/

only ogs remember clankerbotherer@gmail.com
