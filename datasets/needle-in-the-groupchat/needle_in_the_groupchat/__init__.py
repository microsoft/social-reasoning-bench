"""Needle in the Groupchat - Evaluate model recall of user attributions."""

# Evaluation
from .evaluation import (
    ConversationEvaluation,
    ConversationEvaluator,
    DatasetEvaluation,
    DatasetEvaluator,
)

# Formatting
from .formatting import (
    ConversationFormatter,
    MessagesFormatter,
    ToolsFormatter,
)

# Generation
from .generation import (
    ConversationGenerator,
    LLMConversationGenerator,
    PreferenceConversationGenerator,
    RandomConversationGenerator,
)

# Models
from .models import (
    Conversation,
    Dataset,
    EvaluationMode,
    Message,
    MessageFormat,
    NeedlePosition,
    PreferenceConversation,
    User,
)

# Utils
from .utils import TiktokenCounter, TokenCounter

__version__ = "0.1.0"

__all__ = [
    # Evaluation
    "ConversationEvaluation",
    "ConversationEvaluator",
    "DatasetEvaluation",
    "DatasetEvaluator",
    # Formatting
    "ConversationFormatter",
    "MessagesFormatter",
    "ToolsFormatter",
    # Generation
    "ConversationGenerator",
    "LLMConversationGenerator",
    "PreferenceConversationGenerator",
    "RandomConversationGenerator",
    # Models
    "Conversation",
    "Dataset",
    "EvaluationMode",
    "Message",
    "MessageFormat",
    "NeedlePosition",
    "PreferenceConversation",
    "User",
    # Utils
    "TiktokenCounter",
    "TokenCounter",
]
