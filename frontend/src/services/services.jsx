import { v4 as uuidv4 } from "uuid";

const API_URL = "http://localhost:3001/items";

export const getItems = async () => {
  const res = await fetch(API_URL);
  return res.json();
};

export const createItem = async (item, userId) => {
  const now = new Date();
  const newItem = {
    id: uuidv4(),
    ...item,
    user_id: userId,
    is_active: true,
    created_at: now.toISOString(),
    updated_at: now.toISOString()
  };
  
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(newItem),
  });
  return res.json();
};

export const updateItem = async (item) => {
  const now = new Date();
  const updatedItem = {
    ...item,
    updated_at: now.toISOString()
  };
  
  const res = await fetch(`${API_URL}/${item.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(updatedItem),
  });
  return res.json();
};

export const deleteItem = async (id) => {
  const res = await fetch(`${API_URL}/${id}`, {
    method: "DELETE",
  });
  return res.json();
};