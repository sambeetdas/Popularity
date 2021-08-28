class query_handler(object):
    def auth(self, username, password):
        query = f" exec dbo.Valid_User '{username}', '{password}' "
        return query

    def get_all(self):
        query = f" exec dbo.Get_All_Reviews "
        return query

    def insert_model_stat(self, model_code, model_alg, model_type, accuracy):
        query = f" exec dbo.Insert_Model_Stat '{model_code}', '{model_alg}', '{model_type}', '{accuracy}' "
        return query

    def get_all_unmarked_reviews(self):
        query = f" exec dbo.Get_All_Unmarked_Reviews "
        return query    

    def mark_sentiment(self, sentiment, review_id):
        query = f" exec dbo.Marked_Sentiment '{sentiment}', '{review_id}' "
        return query