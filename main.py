from google import genai
import os
import smtplib
import json
from email.message import EmailMessage

if not os.path.isfile('credentials.json'):
    print("Warning! Your credentials.json file doesn't exist. It will be created now.")
    d = {
        "api-key": input("Please enter your Google AI Studio API key (can be created at https://aistudio.google.com/app/api-keys): "),
        "target-gemini-model": "gemini-2.0-flash-exp",
        "sender-email": input("Please enter the bot's email (create a new Gmail account for this): "),
        "sender-app-password": input("Enter the app password for the Gmail account (you can look up how to create this): "),
        "banned-words": [
        ],
        "target-smtp-server": "smtp.gmail.com",
        "target-smtp-port": 587
    }
    with open("credentials.json", "w") as f:
        f.write(json.dumps(d))
        print("Success! Credentials saved to credentials.json.")

data = json.load(open('credentials.json'))

# prompt parameters
name = input("Enter partner's name: ")
responsibility = input("Enter partner's responsibility: ")
banned_words = ", ".join(data["banned-words"])
aggressiveness = input("Enter how aggressive the message should be (1-10): ")
length_of_message = int(input("Enter how long the message should be (number of words, max 500): "))
email = str(input("Enter partner's email: "))

# don't allow the aggressiveness value to exceed 10 and don't allow aggressiveness value to subceed 1
if int(aggressiveness) > 10:
    aggressiveness = 10
elif int(aggressiveness) < 1:
    aggressiveness = 1

# don't allow message length to exceed 500 words (to avoid rate limits) and don't allow message length to subceed 1 word
if length_of_message > 500:
    length_of_message = 500
elif length_of_message < 1:
    length_of_message = 1

# haha funny unobfuscated API key
os.environ["GOOGLE_API_KEY"] = data["api-key"]

# initialize gemini API client
client = genai.Client()

# send content generation request, in this case a prompt that is tweaked by the user input
response = client.models.generate_content(
    model=data["target-gemini-model"],
    contents=f"You play the part of a cartoon bully. Using this persona, write a message to my partner (whose name is {name}) in a group project telling them to get online and work on {responsibility}. The message should have {length_of_message} words. The message should have an aggressiveness level of {aggressiveness}, where 1 is friendly and amicable and 10 is aggressive. Feel free to use insults, but make them humorous and not personal. Do not under any circumstances use the words {banned_words}. Do not include the aggressiveness level in the message.",
)

# uncomment this to print the model's response in the terminal for debug
#print(response.text)

# asynchronously wait for the gemini model to respond with our message
# (i did not write this to be asynchronous, it just did that by itself, which is pretty cool)

#create email object
message = EmailMessage()

# email content
message['Subject'] = f'{responsibility}'
message['From'] = data["sender-email"]
message['To'] = email
message.set_content(response.text)

# email creds
sender_email = data["sender-email"]
password = data["sender-app-password"]  # allow bot to login using an app password instead of a standard one
smtp_server = data["target-smtp-server"]
smtp_port = data["target-smtp-port"] # smtp.gmail.com port 587 is the TLS encryption server, the standard encryption for email

# connect and log in using app password
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls() # start TLS encryption, allowing secure communication
    server.login(sender_email, password)
    server.send_message(message)

print("Email sent successfully!")
