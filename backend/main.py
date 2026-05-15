# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from backend.api.routes import router
# from backend.core.config import Config

# app = FastAPI(title="Document Q&A Engine")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(router, prefix="/api")

# if __name__ == "__main__":
#     import uvicorn
#     Config.validate()
#     uvicorn.run("backend.main:app", host="0.0.0.0", port=8000)




from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Remove "backend." from the imports
from api.routes import router 
from core.config import Config

app = FastAPI(title="Document Q&A Engine")

# ... rest of your middleware code ...

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    Config.validate()
    # Change "backend.main:app" to just "main:app"
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)