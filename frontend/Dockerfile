# Usa Node.js 20 (leve e compatível com Vite)
FROM node:20-alpine

WORKDIR /app

# Copia package.json e package-lock.json (ou pnpm-lock.yaml)
COPY package*.json ./

# Instala dependências
RUN npm install

# Copia o restante do código
COPY . .

EXPOSE 3000

# Comando para rodar o Vite em dev
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
