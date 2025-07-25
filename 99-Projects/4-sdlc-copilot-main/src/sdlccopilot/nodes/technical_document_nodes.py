from typing_extensions import Literal
from langchain_core.messages import AIMessage
from src.sdlccopilot.logger import logging
from src.sdlccopilot.helpers.document import DocumentHelper
from src.sdlccopilot.states.sdlc import SDLCState
from src.sdlccopilot.utils.constants import CONSTANT_TECHNICAL_DOCUMENT, CONSTANT_REVISED_TECHNICAL_DOCUMENT
import os
import time
class TechnicalDocumentNodes:
    def __init__(self, llm):
        self.document_helper = DocumentHelper(llm)
        
    def create_technical_documents(self, state : SDLCState) -> SDLCState:
        logging.info("In create_technical_documents...")
        doc_type = "technical"
        user_stories = state.user_stories
        functional_document = state.functional_documents
        if os.environ.get("PROJECT_ENVIRONMENT") != "development":
            documents = self.document_helper.generate_technical_document_from_llm(functional_document, user_stories)
        else:
            time.sleep(10)
            documents = CONSTANT_TECHNICAL_DOCUMENT
        logging.info("Technical document generated successfully !!!")
        return {
            f"{doc_type}_documents": documents,
            f"{doc_type}_status": 'pending_approval',
            f"{doc_type}_messages": AIMessage(
                content=f"Please review {doc_type} document and provide feedback or type 'Approved' if you're satisfied."
            ),
        }

    def review_technical_documents(self, state : SDLCState) -> SDLCState:
        logging.info("In review_technical_documents...")
        doc_type = "technical"
        user_feedback = state.technical_messages[-1].content.lower().strip()
        logging.info(f"user feedback: {user_feedback}")
        approved = (user_feedback == "approved")
        return {
            f"{doc_type}_messages": AIMessage(
                content="Great! Your technical documents have been finalized. You can now proceed with your next step."
                if approved else
                "I've received your feedback. I'll revise the technical documents accordingly."
            ),
            f"{doc_type}_status": "approved" if approved else "feedback",
        }

    def should_revise_technical_documents(self, state : SDLCState) -> Literal["feedback", "approved"]:
        return "approved" if state.technical_status == "approved" else "feedback" 

    def revise_technical_documents(self, state : SDLCState) -> SDLCState:
        logging.info("In revise_technical_documents...")
        doc_type = "technical"
        user_feedback = state.technical_messages[-2].content.lower().strip()
        logging.info(f"user_feedback : {user_feedback}")
        revised_count = state.revised_count + 1
        logging.info(f"revised_count : {revised_count}")
        if revised_count == 3:
            return {
                f"{doc_type}_messages": AIMessage(
                    content="Technical documents have been revision maxed out. Please review the these documents and continue with the next step."
                ),
                f"{doc_type}_status": "approved",
            }
        if os.environ.get("PROJECT_ENVIRONMENT") != "development":
            documents = self.document_helper.revised_technical_document_from_llm(state.technical_documents, user_feedback)
        else:
            time.sleep(10)
            documents = CONSTANT_REVISED_TECHNICAL_DOCUMENT
        logging.info("Technical document revised successfully !!!")
        return {
            f"{doc_type}_documents": documents,
            f"{doc_type}_messages": AIMessage(
                content=f"Please review revised {doc_type} documents and provide additional feedback or type 'Approved' if you're satisfied."
            ),
            f"{doc_type}_status": "pending_approval",
            "revised_count": revised_count
        }