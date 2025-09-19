from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.models import Service

def get_similar_services(service_id, num_recommendations=4):
    """
    Finds services similar to the given one based on text description.
    """
    try:
        # Get all services from the database
        all_services = Service.objects.all()
        if all_services.count() <= 1:
            return [] # Not enough services to make a recommendation

        # Create a mapping from service ID to its index in the list
        service_list = list(all_services)
        service_id_map = {s.id: i for i, s in enumerate(service_list)}
        
        # Check if the current service is in our list
        if service_id not in service_id_map:
            return []

        # Use TF-IDF to convert service descriptions into numerical vectors
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform([s.description for s in service_list])

        # Calculate cosine similarity between all services
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Get the index of the service we want recommendations for
        service_idx = service_id_map[service_id]

        # Get similarity scores for that service and pair them with their indices
        sim_scores = list(enumerate(cosine_sim[service_idx]))

        # Sort the services based on similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the most similar services, excluding the service itself (which will have a score of 1.0)
        # We start from index 1 to skip the service itself.
        top_similar_indices = [i[0] for i in sim_scores[1:num_recommendations+1]]

        # Return the actual Service objects
        recommended_services = [service_list[i] for i in top_similar_indices]
        
        return recommended_services

    except Exception as e:
        # In case of any error, just return an empty list
        print(f"Error in recommendation engine: {e}")
        return []