import pickle
import numpy as np
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# FastAPI app
app = FastAPI()

# Templates directory
templates = Jinja2Templates(directory="templates")

# Load model and scaler
regmodel = pickle.load(open("regmodel.pkl", "rb"))
scalar = pickle.load(open("scaling.pkl", "rb"))


# Home route - renders the form
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Prediction route for form input
@app.post("/predict_form", response_class=HTMLResponse)
async def predict_form(
    request: Request,
    MedInc: float = Form(...),
    HouseAge: float = Form(...),
    AveRooms: float = Form(...),
    AveBedrms: float = Form(...),
    Population: float = Form(...),
    AveOccup: float = Form(...),
    Latitude: float = Form(...),
    Longitude: float = Form(...),
):
    try:
        data = [
            MedInc,
            HouseAge,
            AveRooms,
            AveBedrms,
            Population,
            AveOccup,
            Latitude,
            Longitude,
        ]
        final_input = scalar.transform(np.array(data).reshape(1, -1))
        output = regmodel.predict(final_input)[0]
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "prediction_text": f"Predicted House Value: ${output:,.2f}",
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html", {"request": request, "prediction_text": f"Error: {str(e)}"}
        )
