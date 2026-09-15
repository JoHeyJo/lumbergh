from strands import Agent, tool
from strands_tools import file_read
from strands_tools.exa import exa_search, exa_get_contents


# Define a custom tool as a Python function using the @tool decorator
@tool
def letter_counter(word: str, letter: str) -> int:
    """
    Count occurrences of a specific letter in a word.

    Args:
        word (str): The input word to search in
        letter (str): The specific letter to count

    Returns:
        int: The number of occurrences of the letter in the word
    """
    if not isinstance(word, str) or not isinstance(letter, str):
        return 0

    if len(letter) != 1:
        raise ValueError("The 'letter' parameter must be a single character")

    return word.lower().count(letter.lower())


# Create an agent with tools from the community-driven strands-tools package
# as well as our custom letter_counter tool
agent = Agent(tools=[exa_search, exa_get_contents])

# Ask the agent a question that uses the available tools
message = """
Can you find all recent software engineer roles posted on https://www.greenhouse.com/careers?
"""
agent(message)
