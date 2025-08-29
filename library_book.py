import asyncio
from connection import config
from agents import Agent, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel


class LibraryBook(BaseModel):
    book_id: str
    book_title: str
    author_name: str
    is_available: bool


library_book = LibraryBook(
    book_id="BOOK-123",
    book_title="Python and AI Programming",
    author_name="John wo",
    is_available=True
)


@function_tool
def get_library_book_info(wrapper: RunContextWrapper[LibraryBook]):
    availability = "available" if wrapper.context.is_available else "not available"
    return f"Book: {wrapper.context.book_title} by {wrapper.context.author_name}, Status: {availability}"

# Main Agent
library_agent = Agent(
    name="LibraryAgent",
    instructions="Answer only library book related questions by using the tool.",
    tools=[get_library_book_info]
)
async def main():
    result = await Runner.run(
        library_agent,
        "Is the Python Programming book available?",
        run_config=config,
        context=library_book
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main()) 