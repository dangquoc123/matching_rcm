import json
import logging

class InputProcessor:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def process(self, file_path: str):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                user_id = data.get("user_id")

                has_search = data.get("search_query") is not None
                has_click = data.get("clicked_product_id") is not None
                has_history = data.get("recent_product_ids") is not None

                fields_set = sum([has_search, has_click, has_history])
                if fields_set != 1:
                    raise ValueError("Loi input.")

                return {
                    "user_id": user_id,
                    "search_query": data.get("search_query"),
                    "clicked_product_id": data.get("clicked_product_id"),
                    "recent_product_ids": data.get("recent_product_ids")
                }

        except Exception as e:
            self.logger.error(f"Lerror when read json file: {e}")
            return None