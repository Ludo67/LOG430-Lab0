import http from 'k6/http';
import { check } from 'k6';
import { uuidv4 } from 'https://jslib.k6.io/k6-utils/1.4.0/index.js';

export const options = {
  stages: [
    { duration: '30s', target: 20 },  // montée progressive
    { duration: '30s', target: 50 },
    { duration: '30s', target: 100 },
    { duration: '30s', target: 150 },
    { duration: '30s', target: 200 },
    { duration: '30s', target: 0 },
  ],
};

let globalOffset = 6;

export default function () {
  const uniqueId = globalOffset + __ITER; // __ITER is local to each VU

  const headers = {
    'Content-Type': 'application/json',
    'X-API-Key': 'topsecret123',
  };

  const payload = JSON.stringify({
    id: uniqueId,
    nom: "ProduitTest",
    categorie: "Test",
    quantite: 100,
    prix: 25.00,
    magasin_id: 2,
  });

  const res = http.post('http://localhost:8080/stock/create', payload, { headers });
  
  check(res, {
    'Produit seedé avec succès (201 ou 200)': (r) => {
    console.log("Status reçu pour création produit:", r.status);
    return r.status === 201 || r.status === 200;
  },
 });

console.log("Body:", res.body);
}
