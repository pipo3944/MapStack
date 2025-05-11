"""
各種ドキュメントのサンプルデータ
"""

documents = [
    {
        "title": "HTMLの基礎",
        "description": "HTMLの基本構造と主要タグの解説",
        "revisions": [
            {
                "version": "1.0.0",
                "change_summary": "初期バージョン",
                "content": {
                    "title": "HTMLの基礎",
                    "sections": [
                        {
                            "title": "HTMLとは",
                            "content": "HTMLはWebページの構造を定義するためのマークアップ言語です。"
                        },
                        {
                            "title": "基本的なHTML文書構造",
                            "content": "HTMLドキュメントは<!DOCTYPE html>宣言から始まり、html、head、bodyタグで構成されます。"
                        }
                    ]
                }
            },
            {
                "version": "1.1.0",
                "change_summary": "セマンティックタグのセクションを追加",
                "content": {
                    "title": "HTMLの基礎",
                    "sections": [
                        {
                            "title": "HTMLとは",
                            "content": "HTMLはWebページの構造を定義するためのマークアップ言語です。"
                        },
                        {
                            "title": "基本的なHTML文書構造",
                            "content": "HTMLドキュメントは<!DOCTYPE html>宣言から始まり、html、head、bodyタグで構成されます。"
                        },
                        {
                            "title": "セマンティックHTML",
                            "content": "セマンティックHTMLとは、タグに意味を持たせることです。例えば、article、section、navなどのタグがあります。"
                        }
                    ]
                }
            }
        ],
        "nodes": ["html-basics", "semantic-html"]
    },
    {
        "title": "CSSスタイリング入門",
        "description": "CSSによるWebページのスタイリング方法",
        "revisions": [
            {
                "version": "1.0.0",
                "change_summary": "初期バージョン",
                "content": {
                    "title": "CSSスタイリング入門",
                    "sections": [
                        {
                            "title": "CSSとは",
                            "content": "CSSはWebページのスタイルを定義するための言語です。"
                        },
                        {
                            "title": "セレクタの基本",
                            "content": "CSSセレクタはスタイルを適用する要素を指定します。"
                        }
                    ]
                }
            }
        ],
        "nodes": ["css-basics"]
    },
    {
        "title": "JavaScriptの基本",
        "description": "JavaScriptプログラミングの基礎知識",
        "revisions": [
            {
                "version": "1.0.0",
                "change_summary": "初期バージョン",
                "content": {
                    "title": "JavaScriptの基本",
                    "sections": [
                        {
                            "title": "JavaScriptとは",
                            "content": "JavaScriptはWebページに動的な機能を追加するためのプログラミング言語です。"
                        },
                        {
                            "title": "変数と定数",
                            "content": "変数はletキーワード、定数はconstキーワードで宣言します。"
                        }
                    ]
                }
            }
        ],
        "nodes": ["js-basics"]
    }
]
