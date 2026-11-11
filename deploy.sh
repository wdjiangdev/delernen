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
#
# 安全措施：
#   - 整个脚本包在 main() 里，最后一行才调用：curl | bash 下载被截断时不会执行半截脚本。
#   - 部署前把当前 www/、nginx.conf、docker-compose.yml 打包到 $DEPLOY_DIR/backup/（保留最近 3 份）。
#   - 健康检查：/、/kurs/、/memorize/、/alice/、/search/index.json 都要 200，/sw.js 的 VERSION 要等于新构建的版本，
#     /kurs 的 301 必须是相对地址。任何一项失败就自动回滚到备份。
#   - 同一个提交连续失败 3 次后，自动部署暂停该提交（.failed_sha），有新提交才再试；手动执行本脚本不受影响。
set -euo pipefail

main() {
REPO="wdjiangdev/delernen"
DEPLOY_DIR="${DEPLOY_DIR:-/opt/docker/delernen}"
PORT="${PORT:-18095}"
REF="${REF:-master}"
AUTO_BIN="${AUTO_BIN:-/usr/local/bin/delernen-autodeploy}"
CRON_FILE="${CRON_FILE:-/etc/cron.d/delernen-autodeploy}"
LOG="/var/log/delernen-deploy.log"
BACKUP_DIR="$DEPLOY_DIR/backup"
KEEP_BACKUPS=3
MAX_FAILS=3

install_auto() {
  # 先写临时文件再 mv（换 inode）：自动部署脚本本身正在执行时也能安全更新它
  cat > "$AUTO_BIN.new" <<EOS
#!/usr/bin/env bash
# DeLernen 自动部署：GitHub master 有新提交时自动部署（由 cron 每 5 分钟调用）
set -euo pipefail
exec 9>/run/delernen-autodeploy.lock
flock -n 9 || exit 0
SHA=\$(curl -fsSL -H 'Accept: application/vnd.github.sha' "https://api.github.com/repos/$REPO/commits/master") || exit 0
[ \${#SHA} -eq 40 ] || exit 0
CUR=\$(cat "$DEPLOY_DIR/.deployed_sha" 2>/dev/null || true)
[ "\$SHA" = "\$CUR" ] && exit 0
# 同一提交连续失败 $MAX_FAILS 次后暂停，等有新提交再试
read -r FSHA FCNT 2>/dev/null < "$DEPLOY_DIR/.failed_sha" || true
if [ "\${FSHA:-}" = "\$SHA" ] && [ "\${FCNT:-0}" -ge $MAX_FAILS ]; then exit 0; fi
echo "[\$(date '+%F %T')] 部署 \$SHA（当前 \${CUR:-无}）"
curl -fsSL "https://raw.githubusercontent.com/$REPO/\$SHA/deploy.sh" | DEPLOY_DIR="$DEPLOY_DIR" PORT="$PORT" REF="\$SHA" bash
EOS
  chmod 755 "$AUTO_BIN.new"
  mv -f "$AUTO_BIN.new" "$AUTO_BIN"
  echo "*/5 * * * * root $AUTO_BIN >> $LOG 2>&1" > "$CRON_FILE.new"
  chmod 644 "$CRON_FILE.new"
  mv -f "$CRON_FILE.new" "$CRON_FILE"
  echo "OK：已开启自动部署（每 5 分钟检查一次），日志：$LOG"
}

case "${1:-}" in
  --remove-auto) rm -f "$CRON_FILE" "$AUTO_BIN"; echo "OK：已关闭自动部署"; return 0 ;;
esac

echo "==> [1/7] 检查 docker / python3"
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

echo "==> [2/7] 下载站点文件（$REF）"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
curl -fsSL "https://codeload.github.com/$REPO/tar.gz/$REF" | tar -xz -C "$TMP"
SRC="$(find "$TMP" -mindepth 1 -maxdepth 1 -type d | head -n1)"
SHA="$REF"
if [ ${#SHA} -ne 40 ]; then
  SHA=$(curl -fsSL -H 'Accept: application/vnd.github.sha' "https://api.github.com/repos/$REPO/commits/$REF" 2>/dev/null || true)
  if [ ${#SHA} -ne 40 ]; then
    # API 失败：codeload 解出的目录名是 <repo>-<完整 sha>，从这里取；还拿不到就记成 unknown（不写分支名）
    SHA="$(basename "$SRC" | grep -oE '[0-9a-f]{40}$' || true)"
    [ -n "$SHA" ] || SHA="unknown-$REF"
  fi
fi

record_fail() {
  local fs fc
  read -r fs fc 2>/dev/null < "$DEPLOY_DIR/.failed_sha" || true
  if [ "${fs:-}" = "$SHA" ]; then fc=$(( ${fc:-0} + 1 )); else fc=1; fi
  echo "$SHA $fc" > "$DEPLOY_DIR/.failed_sha"
  if [ "$fc" -ge "$MAX_FAILS" ]; then
    echo "    提交 ${SHA:0:7} 已连续失败 $fc 次，自动部署暂停此提交（有新提交会再试；手动部署不受影响）"
  fi
}

echo "==> [3/7] 构建（版本号、搜索索引、离线缓存清单）"
python3 "$SRC/scripts/build_site.py" "$SRC" "$TMP/dist"
NEW_VER="$(grep -oE "var VERSION='[^']*'" "$TMP/dist/sw.js" | head -n1 | cut -d"'" -f2)"

mkdir -p "$DEPLOY_DIR/conf" "$DEPLOY_DIR/www" "$BACKUP_DIR"

echo "==> [4/7] 备份当前版本"
BACKUP=""
if [ -n "$(ls -A "$DEPLOY_DIR/www" 2>/dev/null)" ]; then
  BACKUP="$BACKUP_DIR/www-$(date +%Y%m%d-%H%M%S).tgz"
  if [ -f "$DEPLOY_DIR/docker-compose.yml" ]; then
    tar czf "$BACKUP" -C "$DEPLOY_DIR" www conf docker-compose.yml
  else
    tar czf "$BACKUP" -C "$DEPLOY_DIR" www conf
  fi
  echo "    $BACKUP"
  # 只保留最近 $KEEP_BACKUPS 份
  ls -1t "$BACKUP_DIR"/www-*.tgz 2>/dev/null | tail -n +$((KEEP_BACKUPS + 1)) | xargs -r rm -f
else
  echo "    首次部署，没有可备份的内容"
fi

# 把 $1/ 的内容同步到 $2/（删除多余文件）。有 rsync 用 --delay-updates：新文件先写临时名，全部传完再一起改名，
# 尽量缩短“新 HTML 配旧 JSON”的窗口；没有 rsync 时退回 cp + 删除旧文件。只换目录里的文件，不换目录本身（容器挂载不受影响）。
sync_dir() {
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete --delay-updates "$1/" "$2/"
  else
    cp -rf "$1/." "$2/"
    ( cd "$1" && find . -type f | sort ) > "$TMP/sync.lst"
    ( cd "$2" && find . -type f | sort ) | comm -23 - "$TMP/sync.lst" | while read -r f; do rm -f "$2/$f"; done
    find "$2" -mindepth 1 -type d -empty -delete
  fi
}

# nginx.conf 是单文件挂载：必须原地写入（不能 sed -i / mv 换文件），否则容器看到的还是旧文件
write_conf() { touch "$DEPLOY_DIR/conf/nginx.conf"; cat "$1" > "$DEPLOY_DIR/conf/nginx.conf"; }

apply_container() {
  ( cd "$DEPLOY_DIR"
    docker compose up -d --remove-orphans
    if ! docker exec delernen-web cat /etc/nginx/nginx.conf 2>/dev/null | cmp -s - "$DEPLOY_DIR/conf/nginx.conf"; then
      echo "    容器内配置与新配置不一致，重建容器"
      docker compose up -d --force-recreate --remove-orphans
    fi
    if docker exec delernen-web nginx -t >/dev/null 2>&1; then
      docker exec delernen-web nginx -s reload >/dev/null 2>&1 || true
    else
      echo "    nginx -t 未通过："; docker exec delernen-web nginx -t 2>&1 | sed 's/^/      /' || true
      return 1
    fi )
}

# 健康检查：$1 = 期望的 sw.js VERSION（空则不比对）
health() {
  local want="$1" base="http://127.0.0.1:$PORT" u loc ver
  for u in / /kurs/ /memorize/ /alice/ /search/index.json; do
    curl -fs -o /dev/null --max-time 10 "$base$u" || { echo "    健康检查失败：$u"; return 1; }
  done
  # 少斜杠的目录地址必须 301 到相对地址 /kurs/（absolute_redirect off），否则经隧道会跳到内部端口
  loc="$(curl -s -o /dev/null -D - --max-time 10 -H 'Host: delernen.6668800.xyz' "$base/kurs" | tr -d '\r' | awk 'tolower($1)=="location:"{print $2}' || true)"
  [ "$loc" = "/kurs/" ] || { echo "    健康检查失败：/kurs 的 Location 是「$loc」，应为 /kurs/"; return 1; }
  if [ -n "$want" ]; then
    ver="$(curl -fs --max-time 10 "$base/sw.js" | grep -oE "var VERSION='[^']*'" | head -n1 | cut -d"'" -f2 || true)"
    [ "$ver" = "$want" ] || { echo "    健康检查失败：sw.js VERSION=$ver，期望 $want"; return 1; }
  fi
  return 0
}
health_wait() { local i; for i in $(seq 1 15); do health "$1" >/dev/null 2>&1 && return 0; sleep 2; done; health "$1"; }

rollback() {
  if [ -z "$BACKUP" ]; then
    echo "    没有备份可回滚（首次部署），请检查：docker logs delernen-web"
    return 1
  fi
  echo "==> 回滚到 $BACKUP"
  local R="$TMP/rollback"; mkdir -p "$R"
  tar xzf "$BACKUP" -C "$R"
  sync_dir "$R/www" "$DEPLOY_DIR/www"
  [ -f "$R/conf/nginx.conf" ] && write_conf "$R/conf/nginx.conf"
  [ -f "$R/docker-compose.yml" ] && cp -f "$R/docker-compose.yml" "$DEPLOY_DIR/docker-compose.yml"
  chmod -R a+rX "$DEPLOY_DIR/www"
  apply_container || true
  if health_wait ""; then echo "    已回滚，旧版本运行正常"; else echo "    回滚后健康检查仍失败，请检查：docker logs delernen-web"; fi
}

fail() { echo "部署失败：$1"; rollback || true; record_fail; exit 1; }

echo "==> [5/7] 写入 $DEPLOY_DIR"
cp -f "$SRC/deploy/docker-compose.yml" "$DEPLOY_DIR/docker-compose.yml"
sed "s/127.0.0.1:18095/127.0.0.1:$PORT/" "$SRC/deploy/nginx.conf" > "$TMP/nginx.conf"
write_conf "$TMP/nginx.conf"
chmod -R a+rX "$TMP/dist"
sync_dir "$TMP/dist" "$DEPLOY_DIR/www" || fail "复制文件失败"

echo "==> [6/7] 启动容器并重载 nginx 配置"
apply_container || fail "nginx 配置无效"

echo "==> [7/7] 健康检查（/、/kurs/、/memorize/、/alice/、/search/index.json、sw.js 版本 $NEW_VER、/kurs 相对重定向）"
if health_wait "$NEW_VER"; then
  echo "$SHA" > "$DEPLOY_DIR/.deployed_sha"
  rm -f "$DEPLOY_DIR/.failed_sha"
  echo "OK：站点已在 http://127.0.0.1:$PORT 运行（容器 delernen-web，版本 ${SHA:0:7}，sw $NEW_VER）"
  if [ "${1:-}" = "--install-auto" ] || [ -f "$AUTO_BIN" ]; then install_auto; fi
  return 0
fi
fail "健康检查未通过"
}

main "$@"
