/* DeLernen Service Worker：联网时优先取最新内容，断网时用缓存，可整站离线使用。
   部署时 scripts/build_site.py 会填入 VERSION 和 PRECACHE（全站页面与数据），本地开发时为空也能运行。 */
var VERSION='dev';
var PRECACHE=[];
var CACHE='delernen-'+VERSION;
var NET_TIMEOUT=4000; // 网络超过 4 秒且有缓存时，先用缓存

function cacheKey(url){var u=new URL(url);u.search='';u.hash='';return u.href;}

self.addEventListener('install',function(e){
  e.waitUntil(caches.open(CACHE).then(function(c){
    return Promise.all(PRECACHE.map(function(p){
      return fetch(p,{cache:'reload'}).then(function(r){if(r.ok)return c.put(cacheKey(new URL(p,self.location).href),r);}).catch(function(){});
    }));
  }).then(function(){return self.skipWaiting();}));
});
self.addEventListener('activate',function(e){
  e.waitUntil(caches.keys().then(function(ks){
    return Promise.all(ks.filter(function(k){return k.indexOf('delernen-')===0&&k!==CACHE;}).map(function(k){return caches.delete(k);}));
  }).then(function(){return self.clients.claim();}));
});
self.addEventListener('fetch',function(e){
  var req=e.request;
  if(req.method!=='GET')return;
  var url=new URL(req.url);
  if(url.origin!==self.location.origin)return;
  if(url.pathname==='/sw.js')return;
  var key=cacheKey(req.url);
  if(req.mode==='navigate'&&!/\.[a-z0-9]+$/i.test(url.pathname)&&!url.pathname.endsWith('/'))key=cacheKey(url.origin+url.pathname+'/');
  e.respondWith(caches.open(CACHE).then(function(c){
    var net=fetch(req).then(function(r){
      if(r.ok&&r.type==='basic')c.put(key,r.clone());
      return r;
    });
    return c.match(key).then(function(hit){
      if(!hit)return net.catch(function(){
        return req.mode==='navigate'?c.match(cacheKey(url.origin+'/')).then(function(h){return h||Response.error();}):Response.error();
      });
      var timer=new Promise(function(res){setTimeout(function(){res(hit);},NET_TIMEOUT);});
      return Promise.race([net.catch(function(){return hit;}),timer]);
    });
  }));
});
