/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
const VERSION=1,rootPath=self.location.pathname.replace(/\/service-worker.js$/,""),resourceRoot=rootPath+"/vscode-resource",resolveTimeout=3e4;class RequestStore{constructor(){this.map=new Map}get(e,t){const o=this.map.get(this._key(e,t));return o&&o.promise}create(e,t){const o=this.get(e,t);if(o)return o;let n;const s=new Promise(e=>n=e),r={resolve:n,promise:s},i=this._key(e,t);this.map.set(i,r);const a=setTimeout(()=>{if(clearTimeout(a),this.map.get(i)===r)return this.map.delete(i)},resolveTimeout);return s}resolve(e,t,o){const n=this.map.get(this._key(e,t));return!!n&&(n.resolve(o),!0)}_key(e,t){return`${e}@@@${t}`}}const resourceRequestStore=new RequestStore,localhostRequestStore=new RequestStore,notFound=()=>new Response("Not Found",{status:404});async function processResourceRequest(e,t){const o=await self.clients.get(e.clientId);if(!o)return console.log("Could not find inner client for request"),notFound()
;const n=getWebviewIdForClient(o),s=t.pathname.startsWith(resourceRoot+"/")?t.pathname.slice(resourceRoot.length):t.pathname;function r(e){return e?new Response(e.body,{status:200,headers:{"Content-Type":e.mime}}):notFound()}const i=await getOuterIframeClient(n);if(!i)return console.log("Could not find parent client for request"),notFound();const a=resourceRequestStore.get(n,s);return a?a.then(r):(i.postMessage({channel:"load-resource",path:s}),resourceRequestStore.create(n,s).then(r))}async function processLocalhostRequest(e,t){const o=await self.clients.get(e.clientId);if(!o)return;const n=getWebviewIdForClient(o),s=t.origin,r=o=>{if(!o)return fetch(e.request);const n=e.request.url.replace(new RegExp(`^${t.origin}(/|$)`),`${o}$1`);return new Response(null,{status:302,headers:{Location:n}})},i=await getOuterIframeClient(n);if(!i)return console.log("Could not find parent client for request"),notFound();const a=localhostRequestStore.get(n,s);return a?a.then(r):(i.postMessage({channel:"load-localhost",origin:s
}),localhostRequestStore.create(n,s).then(r))}function getWebviewIdForClient(e){return new URL(e.url).search.match(/\bid=([a-z0-9-]+)/i)[1]}async function getOuterIframeClient(e){return(await self.clients.matchAll({includeUncontrolled:!0})).find(t=>{const o=new URL(t.url);return(o.pathname===`${rootPath}/`||o.pathname===`${rootPath}/index.html`)&&o.search.match(new RegExp("\\bid="+e))})}self.addEventListener("message",async e=>{switch(e.data.channel){case"version":return void self.clients.get(e.source.id).then(e=>{e&&e.postMessage({channel:"version",version:1})});case"did-load-resource":{const t=getWebviewIdForClient(e.source),o=e.data.data,n=200===o.status?{body:o.data,mime:o.mime}:void 0;return void(resourceRequestStore.resolve(t,o.path,n)||console.log("Could not resolve unknown resource",o.path))}case"did-load-localhost":{const t=getWebviewIdForClient(e.source),o=e.data.data;return void(localhostRequestStore.resolve(t,o.origin,o.location)||console.log("Could not resolve unknown localhost",o.origin))}}
console.log("Unknown message")}),self.addEventListener("fetch",e=>{const t=new URL(e.request.url);return t.origin===self.origin&&t.pathname.startsWith(resourceRoot+"/")?e.respondWith(processResourceRequest(e,t)):t.origin!==self.origin&&t.host.match(/^localhost:(\d+)$/)?e.respondWith(processLocalhostRequest(e,t)):void 0}),self.addEventListener("install",e=>{e.waitUntil(self.skipWaiting())}),self.addEventListener("activate",e=>{e.waitUntil(self.clients.claim())});
//# sourceMappingURL=https://ticino.blob.core.windows.net/sourcemaps/8795a9889db74563ddd43eb0a897a2384129a619/core/vs/workbench/contrib/webview/browser/pre/service-worker.js.map
