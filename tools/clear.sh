#!/bin/bash

TARGET_DIR="../src"

if [[ ! "$TARGET_DIR" = /* ]]; then
    TARGET_DIR=$(realpath "$TARGET_DIR")
fi

find "$TARGET_DIR" -type d -name "__pycache__" -exec sh -c '
    for dir; do
        echo "正在删除：$dir"
        rm -rf "$dir"
    done' sh {} +

echo "编译缓存清理完毕."
