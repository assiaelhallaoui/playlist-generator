import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

print("NVIDIA_EMBED_MODEL dans .env :", os.environ.get("NVIDIA_EMBED_MODEL"))

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ["NVIDIA_API_KEY"],
)

candidates = sorted(m.id for m in client.models.list().data if "embed" in m.id.lower())
print(f"\n{len(candidates)} modèles contenant 'embed' :\n")

for model in candidates:
    for extra in ({"input_type": "query", "truncate": "END"}, {}):
        try:
            r = client.embeddings.create(
                model=model, input=["test"], encoding_format="float", extra_body=extra
            )
            print(f"OK   {model}  (dim={len(r.data[0].embedding)}, extra_body={bool(extra)})")
            break
        except Exception as e:
            last = str(e)[:80]
    else:
        print(f"FAIL {model}  -> {last}")