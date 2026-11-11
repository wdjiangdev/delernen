#!/usr/bin/env bash
# DeLernen 一键部署脚本（以 root 执行）
#
#   部署/更新到最新版：
#     curl -fsSL https://raw.githubusercontent.com/wdjiangdev/delernen/master/deploy.sh | bash
#   同时开启自动部署（每 5 分钟检查 GitHub，有新提交就自动更新）：
#     curl -fsSL https://raw.githubusercontent.com/wdjiangdev/delernen/master/deploy.sh | bash -s -- --install-auto
#   关闭自动部署：
#     curl -fsSL https://raw.githubusercontent.com/wdjiangdev/delernen/master/deploy.sh | bash -s -- --remove-auto
#
# 部署完成后，在 Cloudflare Tunnel 里加一条 Public Hostname 指向 http://127.0.0.1:18095
set -euo pipefail

REPO="wdjiangdev/delernen"
DEPLOY_DIR="${DEPLOY_DIR:-/opt/docker/delernen}"
PORT="${PORT:-18095}"
REF="${REF:-master}"
AUTO_BIN="/usr/local/bin/delernen-autodeploy"
CRON_FILE="/etc/cron.d/delernen-autodeploy"
LOG="/var/log/delernen-deploy.log"

install_auto() {
  cat > "$AUTO_BIN" <<EOS
#!/usr/bin/env bash
# DeLernen 自动部署：GitHub master 有新提交时自动部署（由 cron 每 5 分钟调用）
set -euo pipefail
exec 9>/run/delernen-autodeploy.lock
flock -n 9 || exit 0
SHA=\$(curl -fsSL -H 'Accept: application/vnd.github.sha' "https://api.github.com/repos/$REPO/commits/master") || exit 0
[ \${#SHA} -eq 40 ] || exit 0
CUR=\$(cat "$DEPLOY_DIR/.deployed_sha" 2>/dev/null || true)
[ "\$SHA" = "\$CUR" ] && exit 0
echo "[\$(date '+%F %T')] 部署 \$SHA（当前 \${CUR:-无}）"
curl -fsSL "https://raw.githubusercontent.com/$REPO/\$SHA/deploy.sh" | DEPLOY_DIR="$DEPLOY_DIR" PORT="$PORT" REF="\$SHA" bash
EOS
  chmod 755 "$AUTO_BIN"
  echo "*/5 * * * * root $AUTO_BIN >> $LOG 2>&1" > "$CRON_FILE"
  chmod 644 "$CRON_FILE"
  echo "OK：已开启自动部署（每 5 分钟检查一次），日志：$LOG"
}

case "${1:-}" in
  --remove-auto) rm -f "$CRON_FILE" "$AUTO_BIN"; echo "OK：已关闭自动部署"; exit 0 ;;
esac

echo "==> [1/6] 检查 docker / python3"
if ! command -v docker >/dev/null 2>&1; then
  echo "    未检测到 docker，正在安装…"
  curl -fsSL https://get.docker.com | sh
fi
if ! docker compose version >/dev/null 2>&1; then
  apt-get update -qq && apt-get install -y -qq docker-compose-plugin
fi
if ! command -v python3 >/dev/null 2>&1; then
  apt-get update -qq && apt-get install -y -qq python3
fi

echo "==> [2/6] 下载站点文件（$REF）"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
curl -fsSL "https://codeload.github.com/$REPO/tar.gz/$REF" | tar -xz -C "$TMP"
SRC="$(find "$TMP" -mindepth 1 -maxdepth 1 -type d | head -n1)"
SHA="$REF"
if [ ${#SHA} -ne 40 ]; then
  SHA=$(curl -fsSL -H 'Accept: application/vnd.github.sha' "https://api.github.com/repos/$REPO/commits/$REF" 2>/dev/null || echo "$REF")
fi

echo "==> [3/6] 构建（版本号、搜索索引、离线缓存清单）"
python3 "$SRC/scripts/build_site.py" "$SRC" "$TMP/dist"

echo "==> [4/6] 写入 $DEPLOY_DIR"
mkdir -p "$DEPLOY_DIR/conf" "$DEPLOY_DIR/www"
cp -f "$SRC/deploy/docker-compose.yml" "$DEPLOY_DIR/docker-compose.yml"
# nginx.conf 是单文件挂载：必须原地写入（不能 sed -i / mv 换文件），否则容器看到的还是旧文件
sed "s/127.0.0.1:18095/127.0.0.1:$PORT/" "$SRC/deploy/nginx.conf" > "$TMP/nginx.conf"
touch "$DEPLOY_DIR/conf/nginx.conf"
cat "$TMP/nginx.conf" > "$DEPLOY_DIR/conf/nginx.conf"
# 先写新文件，再删掉已不存在的旧文件（不替换 www 目录本身，容器挂载不受影响）
cp -rf "$TMP/dist/." "$DEPLOY_DIR/www/"
( cd "$TMP/dist" && find . -type f | sort ) > "$TMP/new.lst"
( cd "$DEPLOY_DIR/www" && find . -type f | sort ) | comm -23 - "$TMP/new.lst" | while read -r f; do rm -f "$DEPLOY_DIR/www/$f"; done
find "$DEPLOY_DIR/www" -mindepth 1 -type d -empty -delete
chmod -R a+rX "$DEPLOY_DIR/www"

echo "==> [5/6] 启动容器并重载 nginx 配置"
cd "$DEPLOY_DIR"
docker compose up -d --remove-orphans
if ! docker exec delernen-web cat /etc/nginx/nginx.conf 2>/dev/null | cmp -s - "$DEPLOY_DIR/conf/nginx.conf"; then
  echo "    容器内配置与新配置不一致，重建容器"
  docker compose up -d --force-recreate --remove-orphans
fi
docker exec delernen-web nginx -t >/dev/null 2>&1 && docker exec delernen-web nginx -s reload >/dev/null 2>&1 || true

echo "==> [6/6] 健康检查"
for i in $(seq 1 15); do
  if curl -fs -o /dev/null "http://127.0.0.1:$PORT/"; then
    echo "$SHA" > "$DEPLOY_DIR/.deployed_sha"
    echo "OK：站点已在 http://127.0.0.1:$PORT 运行（容器 delernen-web，版本 ${SHA:0:7}）"
    if [ "${1:-}" = "--install-auto" ]; then install_auto; fi
    exit 0
  fi
  sleep 2
done
echo "启动失败，请检查：docker logs delernen-web"
exit 1
