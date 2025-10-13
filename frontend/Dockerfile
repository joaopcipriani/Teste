FROM node:20

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

RUN npm install -g serve
EXPOSE 30000
CMD ["serve", "-s", "dist", "-l", "30000"]
