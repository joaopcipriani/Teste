# Use Node LTS oficial (alpine leve)
FROM node:20

WORKDIR /app

# Copia package.json e package-lock.json antes do restante para cache eficiente
COPY package*.json ./

# Instala dependências
RUN npm install

# Copia todos os arquivos (src, vite.config.js, index.html)
COPY . .

# Builda a aplicação
RUN npm run build

# Serve build estático usando serve
RUN npm install -g serve

EXPOSE 30000
CMD ["serve", "-s", "dist", "-l", "30000"]
