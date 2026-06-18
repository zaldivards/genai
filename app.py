from pathlib import Path

from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from api.agent import router as agent_router


def lifespan(*_):
    ingestion_sentinel = Path(".ingestion_complete")
    if not ingestion_sentinel.exists():
        from agent.vectorstore import ingest

        print("Ingesting data...")
        ingest(Path("test_doc.txt").read_text())
        ingestion_sentinel.touch()
        print("Ingestion complete.")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(agent_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8085)
