<?php
$u = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$f = __DIR__ . $u;
if ($u !== '/' && file_exists($f) && !is_dir($f)) return false;
foreach ([$f . '.php', $f . '.html', rtrim($f,'/') . '/index.html'] as $p) {
    if (file_exists($p) && !is_dir($p)) {
        if (substr($p,-4) === '.php') { $_SERVER['SCRIPT_FILENAME']=$p; require $p; return true; }
        return false;
    }
}
return false;
