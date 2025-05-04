# 🌐 Mini Twitter API - Documentação Completa

Esta documentação descreve como interagir com a **Mini Twitter API** para realizar operações relacionadas a usuários, seguidores, posts e likes.

## **Como subir a aplicação**

No diretório raiz

```
 docker-compose up --build
```

## 🔐 **Autenticação**

Todas as requisições que envolvem ações de usuários (criação de posts, seguir usuários, etc.) requerem autenticação via **JWT Token**.

### **Obter o Token de Acesso**

Para obter um token de acesso JWT, envie uma requisição **POST** para o endpoint `/api/v1/token/`.

- **URL:** `/api/v1/token/`
- **Método:** POST
- **Body:**
  ```json
  {
    "username": "johndoe",
    "password": "securepassword"
  }
  ```

## 🔐 **Endpoints da api**

### **Usuários**

Criar um novo usuário

- **URL:** `/api/v1/users/register_user/`
- **Método:** POST
- **Body:**

  ```json
  {
    "username": "joao",
    "email": "joao@email.com",
    "password": "senha"
  }
  ```

Listar todos os usuários

- **URL:** `/api/v1/users/`
- **Método:** GET

Adicionar seguidor

- **URL:** `/api/v1/users/follow/follow_user/`
- **Método:** POST
- **Body:**

  ```json
  {
    "user_id": 1,
    "follower_id": 2
  }
  ```

Remover seguidor

- **URL:** `/api/v1/users/follow/follow_user/`
- **Método:** DELETE
- **Body:**

  ```json
  {
    "user_id": 1,
    "follower_id": 2
  }
  ```

Listar todos os seguidores

- **URL:** `/api/v1/users/follow/get_follow_user/?user_id=id`
- **Método:** GET

### **Postagens**

Criar um novo post

- **URL:** `/api/v1/posts/register_post/`
- **Método:** POST
- **Body:**

  ```json
    "owner": id
    "text": string,
    "image": file,
    "status": int (0,1,2)
  ```

  Lista feed

- **URL:** `/api/v1/posts/get_following_posts/?user_id=id`
- **Método:** GET

### **Curtidas**

Adiciona curtida

- **URL:** `/api/v1/posts/like/like_post/`
- **Método:** POST
- **Body:**

  ```json
    {
  "user": id,
  "post": id
    }
  ```

  Remove curtida

- **URL:** `/api/v1/posts/like/like_post/`
- **Método:** DELETE
- **Body:**

  ```json
    {
  "user": id,
  "post": id
    }
  ```
