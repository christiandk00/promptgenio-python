class PromptGenio:
    def __init__(self, groq_api_key, promptgenio_api_key, tags=None):
        self.client = Groq(api_key=groq_api_key)
        self.logger = logging.getLogger(__name__)
        self.webhook_url = "https://promptgenio.com/api/prompt-logs"
        self.promptgenio_api_key = promptgenio_api_key
        self.tags = tags or {}
        self.latest_log = None  # Store the latest PromptLog instance

    def chat_completion(self, messages, **kwargs):
        # Clear previous additional tags before making a new request
        if self.latest_log:
            self.latest_log.clear_tags()

        try:
            response = self.client.chat.completions.create(messages=messages, **kwargs)
            self.latest_log = self._log_success(messages, response)  # Capture the PromptLog instance
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

        log_id = self._send_log(log_data)  # Capture the log ID
        return PromptLog(log_id=log_id, api_key=self.promptgenio_api_key)  # Return a PromptLog instance

    def _log_error(self, messages, error):
        log_data = {
            "status": "error",
            "messages": messages,
            "error": error,
            "tags": self.tags
        }

        log_id = self._send_log(log_data)  # Capture the log ID
        return PromptLog(log_id=log_id, api_key=self.promptgenio_api_key)  # Return a PromptLog instance

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