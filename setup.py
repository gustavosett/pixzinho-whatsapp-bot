import uvicorn
from app.main import app
from app.services.config import IP, PORT

if __name__ == "__main__":
    # inicia aplicação usando uvicorn
    uvicorn.run(app, host=IP, port=PORT)
