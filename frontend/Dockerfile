# frontend/Dockerfile

# --- Estágio 1: Build com Node.js ---
FROM node:20-alpine AS build-stage

WORKDIR /app

# Copia os arquivos de dependência
COPY package*.json ./

# Instala as dependências
RUN npm ci --only=production=false

# Copia o código fonte do Vue
COPY . .

# Compila para produção (Gera a pasta /dist)
RUN npm run build-only

# --- Estágio 2: Servidor Nginx ---
FROM nginx:alpine AS production-stage

# Copia os arquivos compilados do Vue (pasta dist) para o Nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copia a nossa configuração personalizada do Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Garante que o nginx tem permissões corretas
RUN chmod -R 755 /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]