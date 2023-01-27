from typing import List

import fastapi as _fastapi
import sqlalchemy.orm as _orm
import pandas as pd
import numpy as np

from skforecast.ForecasterAutoreg import ForecasterAutoreg
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

from skforecast.model_selection import grid_search_forecaster
from skforecast.model_selection import backtesting_forecaster
from skforecast.utils import save_forecaster
from skforecast.utils import load_forecaster

import Backend.schemas.purchase_schemas as _schemas
import Backend.schemas.user_schemas as _UserSchemas
import Backend.services.purchase_services as _services
import Backend.services.user_services as _UserService
import Backend.services.customer_services as _CustomerService
from Backend import database

router = _fastapi.APIRouter(
    prefix="/api/analytics",
    tags=['Analytics']
)


@router.get("/")
async def get_analytics(
):
    df = pd.read_sql_query('SELECT * FROM public.purchases', con=database.engine)
    # Feature Generation
    df['Month'] = pd.to_datetime(df['date_created']).dt.month
    df['Year'] = pd.to_datetime(df['date_created']).dt.year
    df['Sales'] = df['quantity'] * df['price']

    # ML Prediction
    y = pd.Series(df.groupby(['Year', 'Month']).sum()['Sales'].tolist())

    regressor = RandomForestRegressor(max_depth=10, n_estimators=100)
    forecaster = ForecasterAutoreg(
        regressor=regressor,
        lags=2
    )

    forecaster.fit(y=y)

    Total_Sales = df.sum()['Sales']
    Predicted_Sales = forecaster.predict(1).tolist()[0]
    Avg_Sales = df.groupby('Month').sum()['Sales'].mean()
    Sales_Month = df.groupby(['Year', 'Month']).sum()['Sales'][-1:].tolist()[0]
    Top_Selling = df.groupby('name').sum()['Sales'].sort_values(ascending=False).head(20).to_json()
    return {
        "Total_Sales": Total_Sales,
        "Predicted_Sales": Predicted_Sales,
        "Avg_Sales": Avg_Sales,
        "Sales_Month": Sales_Month,
        "Top_Selling": Top_Selling
    }
