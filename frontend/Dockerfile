FROM node:20-alpine

WORKDIR /app

# Copia apenas package.json primeiro para instalar dependências
COPY package*.json ./
RUN npm install

# Copia todo o código
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
