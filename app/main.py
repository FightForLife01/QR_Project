# ✅ QR Generator cu PDF stilizat profesional (titlu sub QR în chenar gri)

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fpdf import FPDF
import qrcode
import uuid
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="templates")

QR_DIR = "app/static/qr"
os.makedirs(QR_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "qr_path": None})

@app.post("/generate", response_class=HTMLResponse)
def generate_qr(
    request: Request,
    qr_type: str = Form(...),
    title: str = Form(...),
    data: str = Form(...),
    product: str = Form(...),
    company: str = Form(...),
    address: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    origin: str = Form(...)
):
    if qr_type == "link":
        content = data
    elif qr_type == "email":
        content = f"mailto:{data}"
    elif qr_type == "phone":
        content = f"tel:{data}"
    else:
        content = data

    file_id = uuid.uuid4().hex
    qr_filename = f"{file_id}.png"
    qr_path = os.path.join(QR_DIR, qr_filename)

    img = qrcode.make(content)
    img.save(qr_path)

    # PDF generation cu stil profesional
    pdf_filename = f"{file_id}.pdf"
    pdf_path = os.path.join(QR_DIR, pdf_filename)
    pdf = FPDF()
    pdf.add_page()

    # Inserare cod QR centrat pe pagină
    qr_x = 70
    qr_y = 30
    pdf.image(qr_path, x=qr_x, y=qr_y, w=70, h=70)

    # Titlu în chenar sub cod
    pdf.set_y(qr_y + 75)
    pdf.set_font("Arial", size=14)
    pdf.set_fill_color(180, 180, 180)  # Gri mai închis
    pdf.set_text_color(0)
    pdf.set_draw_color(255)
    pdf.set_line_width(0)
    pdf.cell(0, 10, txt=title, ln=True, align="C", fill=True)

    # Text informativ dedesubt
    pdf.set_font("Arial", size=11)
    pdf.set_y(qr_y + 90)
    details = f"""
{product}
Importator/Distribuitor
{company}
{address}
tel. | {phone}
email | {email}
{origin}
"""
    pdf.multi_cell(0, 8, txt=details.strip(), align="C")
    pdf.output(pdf_path)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "qr_path": f"/static/qr/{qr_filename}",
        "pdf_path": f"/static/qr/{pdf_filename}"
    })