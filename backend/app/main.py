from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from symbols import analyze_stack_text, analyze_minidump


app = FastAPI(title="Stack Translator API")


app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


@app.post('/analyze/text')
async def analyze_text(stack: str = Form(...)):
result = analyze_stack_text(stack)
return JSONResponse(content={"ok": True, "result": result})


@app.post('/analyze/file')
async def analyze_file(dump: UploadFile = File(...)):
content = await dump.read()
try:
result = analyze_minidump(content)
return JSONResponse(content={"ok": True, "result": result})
except Exception as e:
return JSONResponse(status_code=500, content={"ok": False, "error": str(e)})
