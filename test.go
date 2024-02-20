package main

import (
	"fmt"
	"regexp"
)

func main() {
	url := "https://hogehoge.com/gogo/fuga.json?a=b"
	re := regexp.MustCompile(`\/([^\/?#]+)(\?.*)?$`)
	matches := re.FindStringSubmatch(url)

	if len(matches) > 1 {
		fmt.Println("ファイル名:", matches[1]) // ファイル名を出力
	} else {
		fmt.Println("ファイル名が見つかりませんでした。")
	}
}