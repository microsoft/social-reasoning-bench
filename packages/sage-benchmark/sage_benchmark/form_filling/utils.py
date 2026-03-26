"""Utility functions for form filling tasks."""

import ast
import importlib.util
import inspect
from pathlib import Path
from typing import Any

from pydantic import BaseModel


def get_nested_value(data: dict, field_path: str) -> Any:
    """Extract value from nested dict using dot notation.

    Args:
        data: Dictionary to extract from
        field_path: Dot-separated path (e.g., "participant_details.name")

    Returns:
        Value at the specified path, or None if not found

    Example:
        >>> data = {"participant_details": {"name": "John Doe"}}
        >>> get_nested_value(data, "participant_details.name")
        "John Doe"
    """
    keys = field_path.split(".")
    value = data

    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return None

    return value


def import_form_module(form_file_path: str | Path):
    """Dynamically import a form module from a file path.

    Args:
        form_file_path: Path to the Python file containing the form model

    Returns:
        The imported module
    """
    form_file_path = Path(form_file_path)
    module_name = form_file_path.stem

    spec = importlib.util.spec_from_file_location(module_name, form_file_path)
    if spec is None or spec.loader is None:
        raise ValueError(f"Cannot load module from {form_file_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def get_main_form_class(module):
    """Get the main form class from a module.

    The main form class is the LAST BaseModel class defined in the file.
    Uses AST parsing to maintain definition order.

    Args:
        module: The imported module to search

    Returns:
        Tuple of (class_name, class_object)

    Raises:
        ValueError: If no BaseModel classes found or source file cannot be read
    """
    # Get the source file path
    source_file = inspect.getsourcefile(module)
    if not source_file:
        raise ValueError("Cannot find source file for module")

    # Parse the source file with AST to get classes in definition order
    with open(source_file, "r", encoding="utf-8") as f:
        source_code = f.read()

    tree = ast.parse(source_code)

    # Extract class names in definition order
    class_names_in_order = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            # Check if it inherits from BaseModel
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == "BaseModel":
                    class_names_in_order.append(node.name)
                    break

    if not class_names_in_order:
        raise ValueError("No BaseModel classes found in module")

    # Get the last class name (this is the main form class)
    main_class_name = class_names_in_order[-1]

    # Get the actual class object from the module
    if not hasattr(module, main_class_name):
        raise ValueError(f"Class {main_class_name} not found in module")

    main_class = getattr(module, main_class_name)

    # Verify it's a BaseModel subclass
    if not (inspect.isclass(main_class) and issubclass(main_class, BaseModel)):
        raise ValueError(f"{main_class_name} is not a BaseModel subclass")

    return (main_class_name, main_class)


def import_form_model_from_file(model_path: str | Path) -> tuple[str, type[BaseModel]]:
    """Import a pydantic form model from a file and return the main form class.

    This is a convenience function that combines import_form_module and get_main_form_class.

    Args:
        model_path: Path to the form_model.py file

    Returns:
        Tuple of (class_name, class_object)

    Example:
        >>> class_name, form_class = import_form_model_from_file("form_model.py")
        >>> print(class_name)
        "BookingForm"
    """
    module = import_form_module(model_path)
    return get_main_form_class(module)
