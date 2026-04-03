"""Stage 6: Generate interactive HTML form from image + Pydantic model.

Uses a vision model to look at the form image and create matching HTML
that faithfully recreates the paper form's layout with interactive inputs.
"""

from pathlib import Path

from sage_llm import SageMessage, SageModelClient

from sage_data_gen.form_filling.config import FormFillingConfig
from sage_data_gen.form_filling.prompts import GUI_SYSTEM_PROMPT, GUI_USER_PROMPT
from sage_data_gen.form_filling.utils import (
    clean_html_response,
    fix_html,
    image_mime_type,
    image_to_base64,
)


async def _generate_html_async(
    image_path: Path,
    form_model_code: str,
    client: SageModelClient,
    config: FormFillingConfig,
) -> str:
    """Generate HTML form asynchronously.

    Args:
        image_path: Path to the form image.
        form_model_code: Pydantic model code as string.
        client: SageModelClient instance.
        config: Pipeline configuration.

    Returns:
        HTML content as string.
    """
    b64 = image_to_base64(image_path)
    mime = image_mime_type(image_path)

    response = await client.acomplete(
        model=config.vision_model,
        messages=[
            {"role": "system", "content": GUI_SYSTEM_PROMPT},
            {  # type: ignore[list-item]  # multimodal content requires dict format
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": GUI_USER_PROMPT.format(form_model_code=form_model_code),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime};base64,{b64}"},
                    },
                ],
            },
        ],
    )

    content = response.content
    assert isinstance(content, str), "Expected non-streaming text response"
    html_content = clean_html_response(content)

    # Basic validation
    if not html_content.lower().startswith(
        "<!doctype html"
    ) and not html_content.lower().startswith("<html"):
        print("  Warning: HTML response doesn't start with <!DOCTYPE html>")

    return html_content


async def generate_gui_html(
    image_path: Path,
    form_model_code: str,
    client: SageModelClient,
    config: FormFillingConfig,
) -> str:
    """Generate interactive HTML form from image + Pydantic model.

    This is the main entry point for Stage 6.

    Args:
        image_path: Path to the form image.
        form_model_code: Pydantic model code as string.
        client: SageModelClient instance.
        config: Pipeline configuration.

    Returns:
        HTML content as string.
    """
    html_content = await _generate_html_async(image_path, form_model_code, client, config)
    print(f"  Generated {len(html_content)} characters of HTML")

    # Apply CSS fixes for page background
    html_content, changes = fix_html(html_content)
    if changes:
        print(f"  Applied CSS fixes: {', '.join(changes)}")

    return html_content
