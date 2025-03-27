# Use multi-stage build
FROM node:18 as css-builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM python:3.11-slim
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the built CSS and other files
COPY --from=css-builder /app/public/app.css public/app.css
COPY . .

# Run the FastHTML app
CMD ["python", "main.py"] 