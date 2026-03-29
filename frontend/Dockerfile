# FROM node:20.19.1-alpine AS builder

# WORKDIR /app
# COPY package*.json ./
# RUN apk add --no-cache python3 make g++ \
#     && npm ci \
#     && npm cache clean --force

# COPY . .
# RUN npm run build

# FROM nginx:1.25.3-alpine
# RUN rm -rf /usr/share/nginx/html/*
# COPY --from=builder /app/dist /usr/share/nginx/html
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]

# # --- Build Stage gpt ---
# FROM node:20.19.1-bullseye AS builder

# WORKDIR /app
# COPY package*.json ./
# RUN npm ci --omit=dev
# COPY . .
# RUN npm run build

# # --- Production Stage ---
# FROM nginx:1.25.3-alpine

# RUN rm -rf /usr/share/nginx/html/*
# COPY --from=builder /app/dist /usr/share/nginx/html
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]

# syntax=docker/dockerfile:1
# (Is line ko zaroor pehli line banaein)

FROM node:20.19.1-alpine AS builder

WORKDIR /app

# Step 1: Build Tools Install Karein/
RUN apk add --no-cache python3 make g++

# Step 2: Dependencies Files Copy Karein
COPY package*.json ./
# Step 3: Dependencies Install Karein with Caching
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Step 4: Code Copy Aur Build Karein
COPY . .
RUN npm run build


FROM nginx:1.25.3-alpine
RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]