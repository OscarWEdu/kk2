# Run with "uv run fastapi dev main.py"
from utils.config import config
# from api import app
from services.llm_service import SmolLM
from models.llm_model import PromptTemplate

def main():
    llm = SmolLM()

    prompt = PromptTemplate(
        template_str="Tell me a short joke based on {joke1} and {joke2}."
    )

    chain = prompt | llm
    result = chain.invoke(joke1="horses", joke2="pens")

    print(result)


if __name__ == "__main__":
    main()