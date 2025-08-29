import asyncio
from connection import config
from agents import Agent, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel


class BankAccount(BaseModel):
    customer_name: str
    account_number: str
    account_balance: float
    account_type: str

bank_account=BankAccount(
    customer_name="Fatima khan",
    account_number="ACC-789456",
    account_balance=75500.50,
    account_type="savings"
)
@function_tool
def get_user_bank_info(wrapper: RunContextWrapper[BankAccount]):
    acc = wrapper.context
    return (
        f"📌 Bank Account Details\n"
        f"-----------------------------\n"
        f"👤 Account Holder : {acc.customer_name}\n"
        f"🏦 Account Number : {acc.account_number}\n"
        f"💰 Balance        : PKR {acc.account_balance}\n"
        f"📂 Account Type   : {acc.account_type.capitalize()}\n"
        f"-----------------------------\n")

personal_agent = Agent(
    name = "Agent",
    instructions="You are a helpful assistant, always call the tool to get user's information",
    tools=[get_user_bank_info]
)

async def main():
    result = await Runner.run(
        personal_agent, 
        'Please show me a complelet account details', 
        run_config=config,
        context = bank_account #Local context
        )
    print(result.final_output)
if __name__ == "__main__":
    asyncio.run(main()) 