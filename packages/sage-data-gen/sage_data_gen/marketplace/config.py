from pydantic import BaseModel


class MarketplacePipelineConfig(BaseModel):
    output_dir: str = "data/marketplace/final"
    random_seed: int = 42
    total_tasks: int = 280
    small_size: int = 21
    max_rounds: int = 6
    catalog_size: int = 24
    catalog_model: str = "trapi/gpt-4.1"
    context_model: str = "trapi/gpt-4.1"
    max_retries_per_item: int = 3
    max_concurrency: int = 12
