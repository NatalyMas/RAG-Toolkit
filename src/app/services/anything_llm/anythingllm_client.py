import requests


class AnythingLLMClient:
    def __init__(self, base_url: str, api_key: str = "", verify_ssl: bool = False):
        self.base_url = base_url.rstrip('/')
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        self.verify = verify_ssl

    def create_workspace(self, name: str, **kwargs):
        payload = {
            "name": name,
            "similarityThreshold": kwargs.get("similarity_threshold", 0.7),
            "openAiTemp": kwargs.get("temperature", 0.7),
            "openAiHistory": kwargs.get("history_length", 20),
            "chatMode": kwargs.get("chat_mode", "chat"),
            "topN": kwargs.get("top_n", 4)
        }

        if "prompt" in kwargs:
            payload["openAiPrompt"] = kwargs["prompt"]
        if "refusal_response" in kwargs:
            payload["queryRefusalResponse"] = kwargs["refusal_response"]

        response = requests.post(
            f"{self.base_url}/api/workspace/new",
            json=payload,
            headers=self.headers,
            verify=self.verify
        )
        return response.json()

    def add_document(self, workspace_id: str, text: str):
        response = requests.post(
            f"{self.base_url}/api/workspace/{workspace_id}/document",
            json={"text": text},
            headers=self.headers
        )
        return response.json()

    def query(self, workspace_id: str, message: str):
        response = requests.post(
            f"{self.base_url}/api/workspace/{workspace_id}/chat",
            json={"message": message},
            headers=self.headers
        )
        return response.json()
