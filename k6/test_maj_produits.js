import http from 'k6/http';
import { check, sleep } from 'k6';
import { randomSeed, uuidv4 } from 'https://jslib.k6.io/k6-utils/1.4.0/index.js';

export const options = {
  vus: 30,
  duration: '30s',
};

// Fonction exécutée **une seule fois** avant le test
export function setup() {
  const headers = {
    'Content-Type': 'application/json',
    'X-API-Key': 'topsecret123',
  };

  const payload = JSON.stringify({
    id: 6,
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

// Fonction principale exécutée par chaque utilisateur virtuel
export default function () {
  const nom = 'Produit-' + uuidv4().substring(0, 8); // ID unique
  const categorie = ['electronique', 'alimentaire', 'jouet', 'vetement'][Math.floor(Math.random() * 4)];
  const prix = Math.floor(Math.random() * 100) + 1; // entre 1 et 100
  const quantite = Math.floor(Math.random() * 200) + 1; // entre 1 et 200

  const payload = JSON.stringify({
    nom: nom,
    categorie: categorie,
    prix: prix,
    quantite: quantite
  });

  const res = http.put('http://localhost:8080/stock/update/6/magasin/2', payload, {
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': 'topsecret123',
    },
  });

  check(res, {
    'Produit update avec succès (201 ou 200 ou 204)': (r) => {
      console.log("Status update produit", r.status);
      return r.status === 201 || r.status === 200
    },
    });

  sleep(0.5);
}
