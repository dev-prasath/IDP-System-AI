# =========================================================
# backend/api/main.py
# =========================================================

# =========================================================
# IMPORTS
# =========================================================

from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from fastapi.responses import (
    JSONResponse
)

from fastapi.exceptions import (
    RequestValidationError
)

from starlette.exceptions import (
    HTTPException as StarletteHTTPException
)

# =========================================================
# ROUTES
# =========================================================

from backend.api.routes.process_routes import (
    router as process_router
)

from backend.api.routes.document_routes import (
    router as document_router
)

# =========================================================
# LOGGER
# =========================================================

from utils.logger import (

    log_info,

    log_warning,

    log_error,

    log_exception
)

# =========================================================
# DATABASE INITIALIZATION
# =========================================================

from database.postgresql import (
    create_table
)

# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(

    title=(
        "Intelligent Document "
        "Processing API"
    ),

    version="1.0.0",

    description=(

        "AI Powered Intelligent "
        "Document Processing System "
        "using OCR, NLP, Computer Vision, "
        "Table Extraction, and FastAPI"
    )
)

# =========================================================
# DATABASE STARTUP
# =========================================================

create_table()

# =========================================================
# CORS
# =========================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# =========================================================
# STARTUP EVENT
# =========================================================

@app.on_event("startup")
async def startup_event():

    log_info(
        "FastAPI Server Started Successfully"
    )

# =========================================================
# ROOT ENDPOINT
# =========================================================

@app.get("/")
async def root():

    return {

        "success": True,

        "message": (

            "Intelligent Document "
            "Processing API Running "
            "Successfully"
        ),

        "version": "1.0.0",

        "docs": "/docs"
    }

# =========================================================
# STATUS ENDPOINT
# =========================================================

@app.get("/status")
async def status():

    return {

        "success": True,

        "server": "running",

        "ocr": "active",

        "nlp": "active",

        "database": "connected",

        "api": "healthy"
    }

# =========================================================
# HEALTH ENDPOINT
# =========================================================

@app.get("/health")
async def health_check():

    return {

        "success": True,

        "status": "healthy"
    }

# =========================================================
# INCLUDE ROUTERS
# =========================================================

app.include_router(

    process_router,

    tags=["Document Processing"]
)

app.include_router(

    document_router,

    tags=["Document Management"]
)

# =========================================================
# GLOBAL EXCEPTION HANDLER
# =========================================================

@app.exception_handler(Exception)
async def global_exception_handler(

    request,
    exc
):

    log_exception(

        f"Unhandled Exception: "
        f"{str(exc)}"
    )

    return JSONResponse(

        status_code=500,

        content={

            "success": False,

            "message": (
                "Internal Server Error"
            ),

            "error": str(exc)
        }
    )

# =========================================================
# HTTP EXCEPTION HANDLER
# =========================================================

@app.exception_handler(
    StarletteHTTPException
)
async def http_exception_handler(

    request,
    exc
):

    log_error(

        f"HTTP Exception: "
        f"{exc.detail}"
    )

    return JSONResponse(

        status_code=exc.status_code,

        content={

            "success": False,

            "message": exc.detail
        }
    )

# =========================================================
# VALIDATION EXCEPTION HANDLER
# =========================================================

@app.exception_handler(
    RequestValidationError
)
async def validation_exception_handler(

    request,
    exc
):

    log_warning(

        f"Validation Error: "
        f"{str(exc)}"
    )

    return JSONResponse(

        status_code=422,

        content={

            "success": False,

            "message": (
                "Validation Error"
            ),

            "details": exc.errors()
        }
    )

# =========================================================
# REQUEST LOGGER MIDDLEWARE
# =========================================================

@app.middleware("http")
async def log_requests(

    request,
    call_next
):

    log_info(
        f"{request.method} "
        f"{request.url}"
    )

    response = await call_next(
        request
    )

    log_info(

        f"Response Status: "
        f"{response.status_code}"
    )

    return response

# =========================================================
# SHUTDOWN EVENT
# =========================================================

@app.on_event("shutdown")
async def shutdown_event():

    log_info(
        "FastAPI Server Shutdown"
    )