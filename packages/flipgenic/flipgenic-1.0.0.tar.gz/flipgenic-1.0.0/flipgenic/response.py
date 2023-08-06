import random

from flipgenic.db_models import Response
from flipgenic.vector import average_vector


def get_closest_vector(text, index, nlp):
    """
    Get the closest matching response from the index.

    :param text: Text we are comparing against.
    :param index: NGT index to query from.
    :param nlp: Loaded SpaCy model for vectors.
    :returns: Tuple of (id, distance).
    """
    text_vector = average_vector(text, nlp)

    # Nearest neighbour search to find the closest stored vector
    results = index.search(text_vector, 1)
    return results[0] if len(results) else (None, float("inf"))


def get_response(text, index, session, nlp):
    """
    Generate a response to the given text.

    :param text: Text to respond to.
    :param index: NGT index to use for queries.
    :param session: Database session to use for queries.
    :param nlp: Loaded SpaCy model for vectors.
    :returns: Tuple of (response, distance).
    """
    # Find closest matching vector
    match_id, distance = get_closest_vector(text, index, nlp)
    if match_id is None:
        return None, float("inf")

    # Get all response texts associated with this input
    matches = session.query(Response).filter(Response.ngt_id == match_id).all()

    # Select a random response
    responses = [match.response for match in matches]
    response = random.choice(responses)

    return response, distance
