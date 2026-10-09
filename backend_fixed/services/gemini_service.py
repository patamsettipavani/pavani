import json
import re
import traceback
from flask import current_app


def _get_client():
    """Lazily create and return a google-genai Client."""
    api_key = current_app.config.get("GEMINI_API_KEY", "")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    from google import genai
    return genai.Client(api_key=api_key)


def _model_name() -> str:
    return current_app.config.get("GEMINI_MODEL", "gemini-2.5-flash")


def _clean_json_text(raw: str) -> str:
    """Strip markdown code fences if present."""
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def generate_json(prompt: str) -> dict:
    """Call Gemini and return a parsed JSON dict.

    Raises RuntimeError on any failure (API error, bad JSON, empty response).
    """
    try:
        client = _get_client()
        from google.genai import types

        response = client.models.generate_content(
            model=_model_name(),
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        raw_text = response.text
        if not raw_text or not raw_text.strip():
            raise RuntimeError("Gemini returned an empty response.")
        cleaned = _clean_json_text(raw_text)
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        current_app.logger.error("Gemini JSON parse error: %s", exc)
        raise RuntimeError("AI returned invalid JSON.") from exc
    except Exception as exc:
        current_app.logger.error("Gemini API error: %s\n%s", exc, traceback.format_exc())
        raise RuntimeError(f"AI analysis is currently unavailable: {exc}") from exc


def generate_text(prompt: str) -> str:
    """Call Gemini and return raw text."""
    try:
        client = _get_client()
        response = client.models.generate_content(
            model=_model_name(),
            contents=prompt,
        )
        text = response.text
        if not text or not text.strip():
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()
    except Exception as exc:
        current_app.logger.error("Gemini API error: %s\n%s", exc, traceback.format_exc())
        raise RuntimeError(f"AI analysis is currently unavailable: {exc}") from exc