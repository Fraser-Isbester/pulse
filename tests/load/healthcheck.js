import { check, sleep } from 'k6';
import http from 'k6/http';

export let options = {
    vus: 1,
    duration: '30m',
};

export default function () {
    let res = http.get('http://app:8000/');
    check(res, { 'status was 200': (r) => r.status == 200 });
    sleep(5);
}
