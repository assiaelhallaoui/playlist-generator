import os

import numpy as np
from dotenv import load_dotenv
from openai import BadRequestError, OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ["NVIDIA_API_KEY"],
)
EMBED_MODEL = os.environ.get("NVIDIA_EMBED_MODEL", "nvidia/nv-embed-v1")


def _create(batch: list[str], input_type: str):
    try:
        return client.embeddings.create(
            model=EMBED_MODEL,
            input=batch,
            encoding_format="float",
            extra_body={"input_type": input_type, "truncate": "END"},
        )
    except BadRequestError:
        # Certains modèles n'acceptent pas input_type / truncate
        return client.embeddings.create(
            model=EMBED_MODEL,
            input=batch,
            encoding_format="float",
        )


def embed_texts(texts: list[str], input_type: str = "passage") -> np.ndarray:
    """input_type: 'passage' pour les chansons, 'query' pour le scénario."""
    vectors = []
    for i in range(0, len(texts), 32):
        response = _create(texts[i : i + 32], input_type)
        vectors.extend(d.embedding for d in response.data)
    return np.array(vectors)