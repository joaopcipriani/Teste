FROM node:20

WORKDIR /app

# Copiar package.json e package-lock.json primeiro
COPY package*.json ./

# Instala dependências
RUN npm install

# Copiar o restante do código (src, vite.config.js, index.html)
COPY . .

# Build da aplicação
RUN npm run build

# Serve build estático
RUN npm install -g serve

EXPOSE 30000
CMD ["serve", "-s", "dist", "-l", "30000"]
