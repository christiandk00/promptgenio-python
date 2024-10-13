# promptgenio-python


### Send addtional logs
```
# Create an instance of PromptGenio
genio = PromptGenio(groq_api_key='your_groq_api_key', promptgenio_api_key='your_promptgenio_api_key')

# Make a chat completion request
response = genio.chat_completion(messages=["Hello!"], model="llama-3.1-70b-versatile", temperature=0.r)

# Access the latest prompt log and add additional tags
latest_prompt_log = genio.latest_log
latest_prompt_log.add_tag("end_user_reaction", "satisfied")
latest_prompt_log.send_additional_tags()  # Send additional tags to the PromptGenio
```
