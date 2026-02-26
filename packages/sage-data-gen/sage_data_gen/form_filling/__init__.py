"""Form filling data generation package."""

from sage_data_gen.form_filling.config import FormFillingConfig
from sage_data_gen.form_filling.generate_form_task import generate_form_task

__all__ = ["generate_form_task", "FormFillingConfig"]
