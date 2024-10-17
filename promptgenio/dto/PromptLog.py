class PromptLog:
    def __init__(self, log_id, api_key):
        self.log_id = log_id
        self.api_key = api_key
        self.additional_tags = []

    def add_tag(self, key, value):
        self.additional_tags.append({"key": key, "value": value})

    def clear_tags(self):
        self.additional_tags.clear()

    def send_additional_tags(self):
        if not self.log_id:
            raise ValueError("Log ID is not available.")

        url = f"https://promptgenio.com/api/prompt-logs/{self.log_id}/tags"
        data = {
            "tags": self.additional_tags
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()