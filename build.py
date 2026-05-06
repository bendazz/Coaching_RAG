import chromadb

SEPARATOR = "-" * 70

def load_chunks(filename):
    with open(filename) as f:
        text = f.read()
    sections = text.split(SEPARATOR)
    return sections

client = chromadb.PersistentClient("./chroma_db")

files_and_collections = [
    ("opponents_2026.txt", "opponents_2026"),
    ("roster_2026.txt", "roster_2026"),
    ("scouting_2027.txt", "scouting_2027"),
]

for filename, collection_name in files_and_collections:
    chunks = load_chunks(filename)
    collection = client.get_or_create_collection(collection_name)

    ids = []
    for i in range(len(chunks)):
        ids.append(f"chunk_{i}")

    collection.add(documents=chunks, ids=ids)
