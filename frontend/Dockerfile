FROM node:20-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

RUN npm run build
EXPOSE 30000
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "30000"]
