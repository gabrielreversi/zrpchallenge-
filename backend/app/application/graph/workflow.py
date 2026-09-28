from langgraph.graph import END, START, StateGraph

from app.application.graph.nodes import make_nodes
from app.application.graph.state import MatchGraphState
from app.infrastructure.llm.chat import ChatService
from app.infrastructure.llm.embeddings import EmbeddingService
from app.infrastructure.vectorstore.qdrant_client import QdrantCandidateStore


def build_match_graph(
    embeddings: EmbeddingService,
    store: QdrantCandidateStore,
    chat: ChatService,
):
    embed_jd, retrieve_top3, justify_matches = make_nodes(embeddings, store, chat)

    graph = StateGraph(MatchGraphState)
    graph.add_node("embed_jd", embed_jd)
    graph.add_node("retrieve_top3", retrieve_top3)
    graph.add_node("justify_matches", justify_matches)

    graph.add_edge(START, "embed_jd")
    graph.add_edge("embed_jd", "retrieve_top3")
    graph.add_edge("retrieve_top3", "justify_matches")
    graph.add_edge("justify_matches", END)

    return graph.compile()
