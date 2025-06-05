class RecommendationHandler:
    def __init__(self, db_service, embedding_service, matching_service, logger):
        self.db_service = db_service
        self.embedding_service = embedding_service
        self.matching_service = matching_service
        self.logger = logger

    def handle(self, input_data):
        try:
            search_query = input_data.get("search_query")
            clicked_product_id = input_data.get("clicked_product_id")
            recent_product_ids = input_data.get("recent_product_ids")

            query_vector = self.generate_query_vector(
                search_query, clicked_product_id, recent_product_ids
            )

            if query_vector is None:
                self.logger.error("input vector invalid")
                return

            try:
                recommended_products = self.matching_service.find_nearest_products(
                    query_vector, search_query
                )
            except Exception as e:
                self.logger.error(f"error when find nearest products: {e}")
                return

            for product_id in recommended_products:
                try:
                    product = self.db_service.get_product_by_id(product_id)
                    print(f"ProductId: {product_id}")
                    if product:
                        name = product.name if product.name else "N/A"
                        url = product.url if product.url else "N/A"
                        print(f"Name: {name}")
                        print(f"URL: {url}")
                    else:
                        print("Product not found in database.")
                except Exception as e:
                    self.logger.error(f"error when query product id {product_id}: {e}")
        except Exception as e:
            self.logger.error(f"error when process data input: {e}")

    def generate_query_vector(self, search_query, clicked_product_id, recent_product_ids):
        try:
            if search_query:
                return self.embedding_service.embed_search_query(search_query)

            if clicked_product_id:
                try:
                    product = self.db_service.get_product_by_id(clicked_product_id)
                    if product and product.embedding is not None:
                        return product.embedding
                    else:
                        self.logger.warning(f"product vector not found : {clicked_product_id}")
                except Exception as e:
                    self.logger.error(f"Error when find vector embedding product: {e}")

            if recent_product_ids:
                try:
                    products = self.db_service.get_history_product_vectors(recent_product_ids)
                    product_vectors = {
                        p.id: p.embedding for p in products if p.embedding is not None
                    }
                    return self.embedding_service.embed_user_history(
                        recent_product_ids, product_vectors
                    )
                except Exception as e:
                    self.logger.error(f"erorr when process product in history: {e}")

        except Exception as e:
            self.logger.error(f"error when create query vector : {e}")

        return None
