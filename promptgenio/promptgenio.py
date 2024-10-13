import json
import requests
import logging
from groq import Groq

class PromptGenio:
    def __init__(self, groq_api_key, promptgenio_api_key, tags=None):
        self.client = Groq(api_key=groq_api_key)
        self.logger = logging.getLogger(__name__)
        self.webhook_url = "https://promptgenio.com/api/prompt-logs"
        self.promptgenio_api_key = promptgenio_api_key
        self.tags = tags or {}
        self.latest_log_id = None  # Store the latest log ID

    def chat_completion(self, messages, **kwargs):
        try:
            response = self.client.chat.completions.create(messages=messages, **kwargs)
            self._log_success(messages, response)
            return response
        except Exception as e:
            self._log_error(messages, str(e))
            raise

    def _log_success(self, messages, response):
        log_data = {
            "status": "success",
            "messages": messages,
            "response": response.model_dump(),
            "tags": self.tags
        }
        self.latest_log_id = self._send_log(log_data)  # Capture the log ID

    def _log_error(self, messages, error):
        log_data = {
            "status": "error",
            "messages": messages,
            "error": error,
            "tags": self.tags
        }
        self.latest_log_id = self._send_log(log_data)  # Capture the log ID

    def _send_log(self, data):
        try:
            headers = {
                "Authorization": f"Bearer {self.promptgenio_api_key}",
                "Content-Type": "application/json"
            }
            response = requests.post(self.webhook_url, json=data, headers=headers)
            response.raise_for_status()
            return response.json().get('id')  # Return the log ID from the response
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send log: {str(e)}")
            return None  # Return None if sending fails

    def add_tag(self, key, value):
        self.tags[key] = value

    def remove_tag(self, key):
        self.tags.pop(key, None)

    def clear_tags(self):
        self.tags.clear()

    def add_additional_tags(self, additional_tags):
        if not self.latest_log_id:
            self.logger.error("No log ID available to add tags.")
            return

        url = f"https://promptgenio.com/api/prompt-logs/{self.latest_log_id}/tags"
        data = {
            "tags": additional_tags  # Expecting a list of dictionaries with key-value pairs
        }

        try:
            headers = {
                "Authorization": f"Bearer {self.promptgenio_api_key}",
                "Content-Type": "application/json"
            }
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            self.logger.info("Additional tags added successfully.")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to add additional tags: {str(e)}")