from typing import List

class MockVectorStoreTool:
    """
    Mock RAG Vector Store Tool: Simulates querying historical incident logs 
    and matching code fixes using embedding similarity.
    """
    def __init__(self):
        self.knowledge_base = [
            {
                "error_signature": "database connection timeout sql pool exhausted",
                "solution_patch": "increase max_overflow and pool_size in database configuration, and implement connection recycling with pool_pre_ping=True."
            },
            {
                "error_signature": "jwt expired invalid token unauthorized 401",
                "solution_patch": "update token expiration validation window and check clock skew tolerance in auth middleware."
            }
        ]

    def search_similar_logs(self, query: str) -> List[str]:
        query_lower = query.lower()
        results = []
        for item in self.knowledge_base:
            if any(term in query_lower for term in item["error_signature"].split()):
                results.append(item["solution_patch"])
        
        if not results:
            results.append("Standard fallback patch: review application logs, isolate failing service block, and apply unit test coverage.")
        return results

vector_store = MockVectorStoreTool()