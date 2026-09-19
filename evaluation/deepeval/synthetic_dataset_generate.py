from deepeval.synthesizer import Synthesizer
from deepeval.synthesizer.config import ContextConstructionConfig
from typing import List, Optional, Any


class DeepEvalSynthesizer:

    def __init__(self, model: Any,
                 embedder: Optional[Any] = None):
        self.synthesizer = Synthesizer(model=model)
        self.embedder = embedder
        self.model = model

    def generate_goldens_from_documents(self,
                                        document_paths: str,
                                        chunk_size: int = 100,
                                        chunk_overlap: int = 10, ):
        goldens = self.synthesizer.generate_goldens_from_docs(
            document_paths=[document_paths],
            context_construction_config=ContextConstructionConfig(embedder=self.embedder,
                                                                  critic_model=self.model,
                                                                  chunk_size=chunk_size,
                                                                  chunk_overlap=chunk_overlap)
        )
        return goldens

    def to_dataframe(self):
        return self.synthesizer.to_pandas()

    def save_dataset(
            self,
            file_type: str = 'json',
            directory: str = '../../Datasets/synthetic_data',
            file_name: Optional[str] = None,
            quiet: bool = False,
    ):
        self.synthesizer.save_as(
            file_type=file_type,
            directory=directory,
            file_name=file_name,
            quiet=quiet,
        )
