import os

class Generator:
    def __init__(self):
        # No API client needed for the free version
        pass

    def generate_response(self, query, context_items):
        """
        MOCK GENERATION
        Instead of calling OpenAI, we return a formatted string confirming 
        that the retrieval system found the right data.
        """
        
        # 1. Summarize what we found (Proves Retrieval Works)
        context_summary = []
        for item in context_items:
            source = item.get('metadata', {}).get('source', 'Unknown')
            page = item.get('metadata', {}).get('page', 'Unknown')
            context_summary.append(f"- Found content in {source} (Page {page})")
        
        context_str = "\n".join(context_summary)

        # 2. Return a dummy response
        return (
            f"**[FREE MODE] System Operational.**\n\n"
            f"I received your query: '{query}'\n"
            f"I successfully retrieved {len(context_items)} relevant pieces of context:\n"
            f"{context_str}\n\n"
            f"(To generate a real AI answer, a funded OpenAI API Key is required.)"
        )