# coinlens

## Example Coins

1) Elizabeth II 1965 Winston Churchill Crown Coin - £2
2) Henry VIII Hammered Groat Facing Portrait Tower 1544-47 Coin WRL Westair - £10
3) 1917 King George V Half Penny Coin - £1.80
4) Solid Silver 1oz Canadian Maple Leaf 2017 Five Dollars Bullion Coin .9999 Silver - £84
5) Roman imperial coin, Claudius II, 268-270 Antonianus - £15

## Basic Backend Test

Install dependencies
```bash
pip install -r requirements.txt
```

Run the backend application
```bash
coinlens % fastapi run backend.py
```

Send a request to the endpoint
```bash
curl -X 'GET' 'http://0.0.0.0:8000/' -H 'accept: application/json'
```

Ensure the following is received
```
{"message":"Hello, FastAPI!"}
```