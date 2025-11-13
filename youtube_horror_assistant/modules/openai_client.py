"""
OpenAI Client Wrapper for YouTube Horror Assistant
Handles all interactions with OpenAI API
"""

from typing import Optional, Dict, Any, List
import json


class OpenAIClient:
    """Wrapper for OpenAI API interactions"""

    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview", temperature: float = 0.7, max_tokens: int = 4000):
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
            self.model = model
            self.temperature = temperature
            self.max_tokens = max_tokens
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")

    def generate_completion(self, prompt: str, system_message: Optional[str] = None, temperature: Optional[float] = None, max_tokens: Optional[int] = None) -> str:
        """Generate a completion from OpenAI"""
        messages = []

        if system_message:
            messages.append({"role": "system", "content": system_message})

        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature if temperature is not None else self.temperature,
                max_tokens=max_tokens if max_tokens is not None else self.max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def generate_json_completion(self, prompt: str, system_message: Optional[str] = None) -> Dict[str, Any]:
        """Generate a JSON response from OpenAI"""
        full_prompt = prompt + "\n\nPlease respond with valid JSON only."

        response = self.generate_completion(full_prompt, system_message)

        try:
            # Try to extract JSON from markdown code blocks if present
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()

            return json.loads(json_str)

        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON response: {str(e)}\nResponse: {response}")

    def analyze_text_style(self, text: str) -> Dict[str, Any]:
        """Analyze the style and structure of a given text"""
        prompt = f"""Analyze the following text and provide a detailed breakdown of its style and structure:

{text}

Provide a JSON response with the following structure:
{{
    "tone": "description of the tone",
    "pacing": "description of the pacing",
    "vocabulary_level": "simple/intermediate/advanced",
    "sentence_structure": "description",
    "storytelling_techniques": ["technique1", "technique2"],
    "hook_style": "description of how hooks are used",
    "narrative_perspective": "first person/third person/etc",
    "key_stylistic_elements": ["element1", "element2"]
}}"""

        return self.generate_json_completion(prompt)

    def generate_with_style(self, content_prompt: str, style_guide: Dict[str, Any]) -> str:
        """Generate content matching a specific style"""
        system_message = f"""You are a content writer. Generate content matching this style:
Tone: {style_guide.get('tone', 'engaging')}
Pacing: {style_guide.get('pacing', 'moderate')}
Vocabulary: {style_guide.get('vocabulary_level', 'intermediate')}
Techniques: {', '.join(style_guide.get('storytelling_techniques', []))}
"""

        return self.generate_completion(content_prompt, system_message)

    def batch_generate(self, prompts: List[str], system_message: Optional[str] = None) -> List[str]:
        """Generate multiple completions (sequential for now)"""
        results = []

        for prompt in prompts:
            result = self.generate_completion(prompt, system_message)
            results.append(result)

        return results
