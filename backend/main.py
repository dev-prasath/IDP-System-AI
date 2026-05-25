# =========================================================
# IMPORTS
# =========================================================
print("Step 1")
from fastapi import FastAPI  # type: ignore[import]
print("Step 2")
from fastapi.middleware.cors import CORSMiddleware  # type: ignore[import]
print("Step 3")
from fastapi.responses import JSONResponse  # type: ignore[import]
print("Step 4")
from fastapi.exceptions import RequestValidationError  # type: ignore[import]
print("Step 5")
from starlette.exceptions import HTTPException as StarletteHTTPException  # type: ignore[import]
print("Step 6")

# =========================================================
# ROUTES
# =========================================================

from backend.routes.process_routes import (
    router as process_router
)
print("Step 7")
from backend.routes.document_routes import (
    router as document_router
)
print("Step 8")
# =========================================================
# LOGGER
# =========================================================

from utils.logger import (
    log_info,
    log_warning,
    log_error,
    log_exception
)
print("Step 9")
# =========================================================
# FASTAPI APP
# =========================================================

print("STEP 2")
print("STEP 3")
print("STEP 4")


app = FastAPI(

    title="Intelligent Document Processing API",

    version="1.0.0",

    description=(
        "AI Powered Intelligent Document "
        "Processing System using OCR, NLP, "
        "Computer Vision, and FastAPI"
    )
)

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
            "Intelligent Document Processing "
            "API Running Successfully"
        ),

        "version": "1.0.0"
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

# =========================================================
# GLOBAL EXCEPTION HANDLER
# =========================================================

@app.exception_handler(Exception)
async def global_exception_handler(

    request,
    exc
):

    log_exception(
        f"Unhandled Exception: {str(exc)}"
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
        f"HTTP Exception: {exc.detail}"
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
        f"Validation Error: {str(exc)}"
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
        f"{request.method} {request.url}"
    )

    response = await call_next(
        request
    )

    log_info(
        f"Response Status: "
        f"{response.status_code}"
    )

    return response