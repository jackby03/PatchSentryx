import { v4 as uuidv4 } from "uuid";

const API_URL = "http://localhost:3001/firewalls";

export const getFirewalls = async () => {
  const res = await fetch(API_URL);
  return res.json();
};

export const createFirewall = async (firewall, userId) => {
  const now = new Date();
  const newFirewall = {
    id: uuidv4(),
    ...firewall,
    collection_id: userId,
    is_active: true,
    created_at: now.toISOString(),
    updated_at: now.toISOString()
  };
  
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(newFirewall),
  });
  return res.json();
};

export const updateFirewall = async (firewall) => {
  const now = new Date();
  const updatedFirewall = {
    ...firewall,
    updated_at: now.toISOString()
  };
  
  const res = await fetch(`${API_URL}/${firewall.id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(updatedFirewall),
  });
  return res.json();
};

export const deleteFirewall = async (id) => {
  const res = await fetch(`${API_URL}/${id}`, {
    method: "DELETE",
  });
  return res.json();
};