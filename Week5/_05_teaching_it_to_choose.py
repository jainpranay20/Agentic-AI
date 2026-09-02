"""Letting the model choose a tool for itself, via a tool schema.

Needs an OpenAI-compatible provider (Groq, OpenRouter, or OpenAI) --
Anthropic's tool-calling API uses a different response shape, covered
in a later module.

Setup: uv add openai python-dotenv
.env:  set at least one of GROQ_API_KEY / OPENROUTER_API_KEY / OPENAI_API_KEY
"""

import json  # used to parse JSON arguments returned by the model
import os  # used to read API keys from environment variables

from dotenv import load_dotenv  # reads .env file into os.environ

load_dotenv()  # load values from .env, so os.environ["OPENAI_API_KEY"] etc. work


SAMPLE_WEATHER = {
    "tokyo": {"celsius": 22, "conditions": "partly cloudy"},  # sample data for Tokyo
    "delhi": {"celsius": 34, "conditions": "clear skies"},    # sample data for Delhi
    "london": {"celsius": 15, "conditions": "light rain"},    # sample data for London
}


def get_weather(city: str) -> str:
    """Same tool as File 4 -- a plain function, unaware that an AI exists."""
    data = SAMPLE_WEATHER.get(city.lower())  # lookup weather by lowercase city
    if data is None:
        return f"No weather data for {city!r}."  # if city not found, return this
    return f"{city.title()}: {data['celsius']}C, {data['conditions']}"  
    # example return: "Tokyo: 22C, partly cloudy"


# The "menu" handed to the model. It never sees get_weather() itself --
# only this description. The wording of "description" is what tells the
# model when this tool is relevant to a given question.
get_weather_schema = {
    "type": "function",
    "function": {
        "name": "get_weather",  # tool name the model may choose
        "description": "Get the current weather for a city. Use this whenever "
                        "the user asks about weather, temperature, or conditions "
                        "in a specific place.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city name, e.g. 'Tokyo'."}
            },
            "required": ["city"],  # model must return a city field if it chooses this tool
        },
    },
}


def get_client_and_model():
    """Picks whichever OpenAI-compatible provider has a key set. Raises
    clearly if none is configured, since real decision-making genuinely
    needs a real model to call.
    """
    from openai import OpenAI  # imported here only when needed

    if os.environ.get("GROQ_API_KEY"):  # if GROQ key exists
        return (
            OpenAI(api_key=os.environ["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1"),
            "llama-3.3-70b-versatile",
        )  # return Groq-compatible client and model
    if os.environ.get("OPENROUTER_API_KEY"):  # if OpenRouter key exists
        return (
            OpenAI(api_key=os.environ["OPENROUTER_API_KEY"], base_url="https://openrouter.ai/api/v1"),
            "openrouter/free",
        )  # return OpenRouter-compatible client and model
    if os.environ.get("OPENAI_API_KEY"):  # if OpenAI key exists
        return OpenAI(api_key=os.environ["OPENAI_API_KEY"]), "gpt-4o-mini"  
        # return OpenAI client and model

    raise RuntimeError(
        "No OpenAI-compatible key found. Set one of GROQ_API_KEY, "
        "OPENROUTER_API_KEY, or OPENAI_API_KEY in your .env file."
    )  # if none configured, fail immediately


def ask_ai_to_choose(question: str):
    """Sends the question plus the tool schema in one call. The reply may
    contain a tool_calls list instead of plain text -- that list is the
    model's decision, not an executed result.
    """
    client, model = get_client_and_model()  # pick provider and model
    response = client.chat.completions.create(
        model=model,
        max_tokens=300,
        messages=[{"role": "user", "content": question}],  # user's question
        tools=[get_weather_schema],  # expose the tool schema to the model
    )
    return response.choices[0].message  # return the model's message object


if __name__ == "__main__":
    question = "What's the weather like in Tokyo right now?"  # sample question
    message = ask_ai_to_choose(question)  # ask model to choose a tool

    if message.tool_calls:  # if the model chose a tool call
        call = message.tool_calls[0]  # first tool call
        arguments = json.loads(call.function.arguments)  
        # parse arguments like '{"city":"Tokyo"}' into {"city": "Tokyo"}
        result = get_weather(**arguments)  # call tool with parsed args
        print(f"{call.function.name}({arguments}) -> {result}")
        # example printed output:
        # get_weather({'city': 'Tokyo'}) -> Tokyo: 22C, partly cloudy
    else:
        print(message.content)  # if no tool call, print plain text response
        # example output if model did not choose tool: "I think the weather in Tokyo is..."