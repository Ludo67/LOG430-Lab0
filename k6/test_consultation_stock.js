import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 50, // utilisateurs simultanés
  duration: '30s',
};

export default function () {
  const magasinIds = [1, 2, 3, 4, 5];
  magasinIds.forEach(id => {
    const res = http.get(`http://localhost:8080/restock/stock_par_magasin?magasin_id=${id}`, {
      headers: { 'X-API-Key': 'topsecret123' }
    });
    check(res, { 'status is 200': (r) => r.status === 200 });
  });
  sleep(1);
}
