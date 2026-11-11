/* DeLernen Service Worker：联网时优先取最新内容，断网时用缓存，可整站离线使用。
   部署时 scripts/build_site.py 会填入 VERSION 和 PRECACHE（全站页面与数据），本地开发时为空也能运行。 */
var VERSION='dev';
var PRECACHE=[];
var SW_REV=2; // 改了 SW 逻辑时手动加 1（缓存名随之变化，旧缓存在 activate 时清掉）
var CACHE='delernen-'+VERSION+'-r'+SW_REV;
var NET_TIMEOUT=4000; // 网络超过 4 秒且有缓存时，先用缓存

// 缓存 key：去掉 ?v= 和 #hash；/x/index.html 与 /x/ 是同一页面，统一存成 /x/
function cacheKey(url){var u=new URL(url);u.search='';u.hash='';u.pathname=u.pathname.replace(/\/index\.html$/,'/');return u.href;}
// 不带斜杠、也没有扩展名的目录地址（如 /kurs/a1）
function isDirNoSlash(p){return !p.endsWith('/')&&!/\.[a-z0-9]+$/i.test(p);}

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
  // 导航到 /kurs/a1 这类地址：直接 301 到 /kurs/a1/，让地址栏带上斜杠，页面里的相对路径（fetch('x.json')）才能解析对；
  // 也避开“fetch 跟随 301 后拿 redirected 响应回应导航请求”在 Chrome/Safari 上报网络错误的问题。
  if(req.mode==='navigate'&&isDirNoSlash(url.pathname)){
    e.respondWith(Response.redirect(url.origin+url.pathname+'/'+url.search+url.hash,301));
    return;
  }
  var key=cacheKey(req.url);
  e.respondWith(caches.open(CACHE).then(function(c){
    var net=fetch(req).then(function(r){
      if(r.redirected){
        // 被重定向过的响应不能直接回应导航请求，重新包一层；也不写进缓存（key 和最终地址对不上）
        return new Response(r.body,{status:r.status,statusText:r.statusText,headers:r.headers});
      }
      if(r.ok&&r.type==='basic')e.waitUntil(c.put(key,r.clone()).catch(function(){}));
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
