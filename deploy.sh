#!/usr/bin/env bash
# DeLernen 一键部署脚本
# 在新服务器上以 root 执行一次即可：
#   curl -fsSL https://raw.githubusercontent.com/wdjiangdev/delernen/master/deploy.sh | bash
# 或： bash deploy.sh
# 部署完成后，在 Cloudflare Tunnel 里加一条 Public Hostname 指向 http://127.0.0.1:18095
set -euo pipefail

DEPLOY_DIR="${DEPLOY_DIR:-/opt/docker/delernen}"
PORT="${PORT:-18095}"
REPO_TARBALL="https://github.com/wdjiangdev/delernen/archive/refs/heads/master.tar.gz"

echo "==> [1/5] 检查 docker"
if ! command -v docker >/dev/null 2>&1; then
  echo "    未检测到 docker，正在安装…"
  curl -fsSL https://get.docker.com | sh
else
  echo "    $(docker --version)"
fi
if ! docker compose version >/dev/null 2>&1; then
  echo "    安装 docker compose 插件…"
  apt-get update -qq && apt-get install -y -qq docker-compose-plugin
fi

echo "==> [2/5] 下载站点文件"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
curl -fsSL "$REPO_TARBALL" | tar -xz -C "$TMP"
SRC="$TMP/delernen-master"

echo "==> [3/5] 写入 $DEPLOY_DIR"
mkdir -p "$DEPLOY_DIR/conf" "$DEPLOY_DIR/www"
cp -f "$SRC/deploy/docker-compose.yml" "$DEPLOY_DIR/docker-compose.yml"
cp -f "$SRC/deploy/nginx.conf" "$DEPLOY_DIR/conf/nginx.conf"
# 监听端口可通过 PORT 环境变量覆盖
sed -i "s/127.0.0.1:18095/127.0.0.1:$PORT/" "$DEPLOY_DIR/conf/nginx.conf"
# 同步网站文件（排除构建脚本与部署文件）
cp -rf "$SRC/index.html" "$SRC/a1a2" "$SRC/a1b2" "$SRC/grammatik" "$SRC/a1-kurs" "$SRC/a2-kurs" "$DEPLOY_DIR/www/"
chmod -R a+rX "$DEPLOY_DIR/www"

echo "==> [4/5] 启动容器"
cd "$DEPLOY_DIR"
docker compose up -d --remove-orphans

echo "==> [5/5] 健康检查"
for i in $(seq 1 15); do
  if curl -fs -o /dev/null "http://127.0.0.1:$PORT/"; then
    echo "OK：站点已在 http://127.0.0.1:$PORT 运行（容器 delernen-web）"
    echo ""
    echo "下一步：在 Cloudflare Tunnel 添加 Public Hostname，"
    echo "      指向 Service http://127.0.0.1:$PORT"
    exit 0
  fi
  sleep 2
done
echo "启动失败，请检查：docker logs delernen-web"
exit 1
