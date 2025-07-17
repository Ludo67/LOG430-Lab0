import http from 'k6/http';
import { check } from 'k6';

export let options = {
  vus: 10,
  duration: '30s',
};

export default function () {
  const res = http.get('http://host.docker.internal:8082/cart/whoami', {
    headers: { 'X-API-Key': 'topsecret123' },
  });
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
}
