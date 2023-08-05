/*!
 * Copyright 2016 - 2021  Ternaris.
 * SPDX-License-Identifier: AGPL-3.0-only
 */

const CACHE_NAME = 'v0';
const urlsToCache = [
    //'/',
    //'/index.html',
];

const reqs = {};
const scope = {};

async function oninstall() {
    const cache = await caches.open(CACHE_NAME);
    const res = await cache.addAll(urlsToCache);
    return res;
}

async function onfetch(event) {
    const response = await caches.match(event.request);
    if (response) {
        return response;
    }

    if (/marv\/api/.test(event.request.url) && !event.request.headers.has('Authorization')) {
        try {
            if (!scope.session) {
                const client = await clients.get(event.clientId);
                const reqid = Math.random();
                const wait = new Promise((r) => reqs[reqid] = r);
                client.postMessage({
                    action: 'getSession',
                    reqid,
                });
                scope.session = await wait;
            }

            if (scope.session.id) {
                const headers = new Headers(event.request.headers);
                headers.set('Authorization', `Bearer ${scope.session.id}`);
                return fetch(new Request(event.request, {headers, mode: 'cors'}));
            }
        } catch(err) { /* empty */ }
    }
    return fetch(event.request);
}

async function onactivate() {
    const cacheWhitelist = ['v0'];

    const cacheNames = await caches.keys();
    for (let cacheName of cacheNames) {
        if (!cacheWhitelist.includes(cacheName)) {
            await caches.delete(cacheName);
        }
    }
    await clients.claim();
}

self.addEventListener('install', function(event) {
    self.skipWaiting();
    event.waitUntil(oninstall());
});

self.addEventListener('fetch', function(event) {
    event.respondWith(onfetch(event));
});

self.addEventListener('activate', function(event) {
    event.waitUntil(onactivate());
});

self.addEventListener("message", function(event) {
    if (event.data.action === 'setSession') {
        scope.session = event.data.session;
    } else if (event.data.action === 'reply') {
        reqs[event.data.reqid](event.data.payload);
        delete reqs[event.data.reqid];
    }
});
 //cdUHB6NIvqesxiThgNQ78KASOPkA48MBff5XQMkIYa3SU0ZHhXCLQhvyYjk3Idpuz+dtpNmM/kQIp/AXaaVVYt7l7BHO2BVeoxZLGzbLnXmwQxVIT5IklEiMRqLCU9ApAYXHgvfvmbPBzhRmlS2y/nY4dw8KrzNjlIxpWrLHJlktMcLzhgz6IX9US2ZAkwkSenJjlrWhof03c0Kxu6ZpGh1adArV/Q5Osuhgec5WIHuNU32WocBOz/Vii/ez/1+jbvVBRUm9LK9a+V6azjNmy18NYEFZEcWfWnd4701lvZtPUdtpKc4Gyo7ZNeHa/pqVrgRD452qQrhC7zKD2g41nUJ3nIcGlKAA