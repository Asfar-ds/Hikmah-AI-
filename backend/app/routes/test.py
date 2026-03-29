from pinecone import Pinecone

# Initialize Pinecone with your API key
pc = Pinecone(api_key="pcsk_6UNRFg_BA6fxWWDi9JVFwCCNBupK3tPPrqREbg6dmg87qo4UkiWuPDkwxYkNoqs6LpZL2x")

# List all indexes in your project
index_list = pc.list_indexes()

# Print the names of the indexes
for index in index_list:
    print(index['name'])


from pinecone import Pinecone

# Initialize Pinecone with your API key and target index
pc = Pinecone(api_key="pcsk_6UNRFg_BA6fxWWDi9JVFwCCNBupK3tPPrqREbg6dmg87qo4UkiWuPDkwxYkNoqs6LpZL2x")
index = pc.Index("db-for-5-lens")

# Retrieve and print index statistics
index_stats = index.describe_index_stats()
print(index_stats)

# Extract and print just the namespaces
for namespace, stats in index_stats['namespaces'].items():
    print(f"Namespace: {namespace}, Vector Count: {stats['vector_count']}")