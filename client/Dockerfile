FROM node:22-slim

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 5173
# use Vite - "npm run dev"
CMD ["npm", "run", "dev", "--", "--host"]