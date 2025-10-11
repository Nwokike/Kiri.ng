import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.models import Service

logger = logging.getLogger(__name__)

def get_similar_services(service, num_recommendations=4):
    """
    Finds services similar to the given one, prioritizing services
    within the same category first.
    """
    try:
        # Step 1: Find other services in the same category.
        same_category_services = Service.objects.filter(category=service.category).exclude(id=service.id)

        # If there are not enough services in the same category, we stop here for now.
        # A future improvement could be to then look at all other services.
        if same_category_services.count() == 0:
            return []

        # Combine the target service with the candidates for TF-IDF calculation
        services_to_compare = [service] + list(same_category_services)
        
        # Use TF-IDF to convert service descriptions into numerical vectors
        tfidf = TfidfVectorizer(stop_words='english')
        # We only use the descriptions for similarity calculation
        descriptions = [s.description for s in services_to_compare]
        tfidf_matrix = tfidf.fit_transform(descriptions)

        # Calculate cosine similarity. The first item (index 0) is our target service.
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)

        # Get the similarity scores for our target service against all others.
        # We get the first (and only) row of the similarity matrix.
        sim_scores = list(enumerate(cosine_sim[0]))

        # Sort the services based on similarity scores in descending order.
        # We skip index 0 because it's the service itself (score of 1.0).
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:]

        # Get the indices of the top N most similar services.
        top_similar_indices = [i[0] for i in sim_scores[:num_recommendations]]

        # Return the actual Service objects based on the sorted indices.
        # Note: The indices from sim_scores refer to the `services_to_compare` list.
        recommended_services = [services_to_compare[i] for i in top_similar_indices]
        
        return recommended_services

    except Exception as e:
        # In case of any error, just return an empty list to prevent crashes.
        logger.error(f"Error in recommendation engine: {e}")
        return []
