import uvicorn
from fastapi import FastAPI

from api.auth import router as auth_router
from moex_parser.data_endpoints import router as data_router
from auth.auth_middleware import JWTAuthMiddleware

app = FastAPI(title='StockAnalysis')

app.add_middleware(JWTAuthMiddleware)

app.include_router(auth_router, prefix='/api')
app.include_router(data_router, prefix='/data')

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='0.0.0.0',
        port=8000,
        reload=True
    )
