import asyncio
from connection import config
from agents import Agent, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel


class StudentProfile(BaseModel):
    student_id: str
    student_name: str
    current_semester: int
    total_courses: int

student_info=StudentProfile(
    student_id="STU-456",
    student_name="Hassan Ahmed",
    current_semester=4,
    total_courses=5
)

@function_tool
def get_student_info(wrapper: RunContextWrapper[StudentProfile]):
    st=wrapper.context
    return(
         f"🎓 Student Profile\n"
         f"-----------------------------\n"
        f"🆔 Student ID     : {st.student_id}\n"
        f"👤 Name           : {st.student_name}\n"
        f"📚 Semester       : {st.current_semester}\n"
        f"📖 Total Courses  : {st.total_courses}\n"
        f"-----------------------------"
    )

personal_agent = Agent(
    name = "Agent",
    instructions="You are a helpful assistant, always call the tool to get user's information",
    tools=[get_student_info]
)

async def main():
    result = await Runner.run(
        personal_agent,  
        "Show me my complete student profile",
         run_config=config,
        context = student_info#Local context
        )
    print(result.final_output)
if __name__ == "__main__":
    asyncio.run(main()) 