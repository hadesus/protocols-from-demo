# Этап сборки
FROM node:20-alpine as build

WORKDIR /app

# Устанавливаем pnpm
RUN npm install -g pnpm

# Копируем файлы зависимостей
COPY package.json pnpm-lock.yaml ./

# Устанавливаем зависимости
RUN pnpm install --frozen-lockfile

# Копируем конфигурационные файлы
COPY vite.config.js jsconfig.json components.json ./

# Копируем исходный код
COPY src/ ./src/
COPY public/ ./public/
COPY index.html ./

# Собираем приложение
RUN pnpm run build

# Этап production
FROM nginx:alpine

# Копируем собранное приложение
COPY --from=build /app/dist /usr/share/nginx/html

# Копируем конфигурацию nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Открываем порт
EXPOSE 80

# Команда запуска
CMD ["nginx", "-g", "daemon off;"]

