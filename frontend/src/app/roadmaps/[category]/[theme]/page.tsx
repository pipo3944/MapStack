'use client';

import { nodeTypes } from '@/components/roadmap/RoadmapNodes';
import Link from 'next/link';
import { useParams, useRouter } from 'next/navigation';
import { useCallback, useEffect, useState } from 'react';
import ReactFlow, {
  Background,
  Controls,
  Edge,
  MiniMap,
  Node,
  NodeTypes,
  Panel,
  useEdgesState,
  useNodesState,
} from 'reactflow';
import 'reactflow/dist/style.css';

// ロードマップのデータ型定義
interface RoadmapNode {
  id: string;
  title: string;
  description: string;
  status?: 'not-started' | 'in-progress' | 'completed' | 'skipped';
  type?: 'primary' | 'secondary' | 'recommended' | 'optional';
  children?: RoadmapNode[];
  resources?: {
    title: string;
    url: string;
    type: 'article' | 'video' | 'course' | 'book' | 'docs';
  }[];
}

interface RoadmapData {
  id: string;
  title: string;
  description: string;
  categoryId: string;
  categoryTitle: string;
  themeId: string;
  themeTitle: string;
  nodes: RoadmapNode[];
}

// カスタムノードタイプを統合
const customNodeTypes: NodeTypes = {
  ...nodeTypes,
};

// フロントエンドロードマップのノードデータ
const getFrontendNodesAndEdges = () => {
  const nodes: Node[] = [
    {
      id: 'internet',
      type: 'primary',
      data: {
        label: 'インターネット',
        description: 'インターネットの仕組み、ブラウザの動作原理、HTTP/HTTPSプロトコルについて学ぶ',
        nodeId: 'internet',
      },
      position: { x: 250, y: 0 },
    },
    {
      id: 'html',
      type: 'primary',
      data: {
        label: 'HTML',
        description: 'HTMLの基本構造、セマンティックHTML、フォーム、アクセシビリティについて学ぶ',
        nodeId: 'html',
      },
      position: { x: 100, y: 100 },
    },
    {
      id: 'css',
      type: 'primary',
      data: {
        label: 'CSS',
        description: 'CSSの基本、レイアウト、レスポンシブデザイン、アニメーションについて学ぶ',
        nodeId: 'css',
      },
      position: { x: 250, y: 100 },
    },
    {
      id: 'javascript',
      type: 'primary',
      data: {
        label: 'JavaScript',
        description: 'JavaScriptの基本文法、DOM操作、非同期処理、ES6+の機能について学ぶ',
        nodeId: 'javascript',
      },
      position: { x: 400, y: 100 },
    },
    {
      id: 'how-internet-works',
      type: 'secondary',
      data: {
        label: 'インターネットの仕組み',
        description: 'ネットワーク、DNS、ホスティング、ブラウザの基本概念',
        nodeId: 'how-internet-works',
      },
      position: { x: -60, y: -20 },
    },
    {
      id: 'http',
      type: 'secondary',
      data: {
        label: 'HTTP/HTTPS',
        description: 'HTTPメソッド、ステータスコード、ヘッダー、セキュリティ',
        nodeId: 'http',
      },
      position: { x: 0, y: 40 },
    },
    {
      id: 'html-basics',
      type: 'secondary',
      data: {
        label: 'HTML基礎',
        description: 'タグ、要素、属性、構造化',
        nodeId: 'html-basics',
      },
      position: { x: 0, y: 180 },
    },
    {
      id: 'semantic-html',
      type: 'secondary',
      data: {
        label: 'セマンティックHTML',
        description: '意味のあるHTMLタグの使用方法',
        nodeId: 'semantic-html',
      },
      position: { x: 0, y: 250 },
    },
    {
      id: 'forms-validation',
      type: 'secondary',
      data: {
        label: 'フォームとバリデーション',
        description: 'フォーム要素、入力検証、ユーザビリティ',
        nodeId: 'forms-validation',
      },
      position: { x: 0, y: 320 },
    },
    {
      id: 'accessibility',
      type: 'recommended',
      data: {
        label: 'アクセシビリティ',
        description: 'WAI-ARIA、キーボードナビゲーション、スクリーンリーダー対応',
        nodeId: 'accessibility',
      },
      position: { x: 0, y: 390 },
    },
    {
      id: 'css-basics',
      type: 'secondary',
      data: {
        label: 'CSS基礎',
        description: 'セレクタ、プロパティ、値、ボックスモデル',
        nodeId: 'css-basics',
      },
      position: { x: 200, y: 180 },
    },
    {
      id: 'layout',
      type: 'secondary',
      data: {
        label: 'レイアウト',
        description: 'フレックスボックス、グリッド、ポジショニング',
        nodeId: 'layout',
      },
      position: { x: 200, y: 250 },
    },
    {
      id: 'responsive-design',
      type: 'secondary',
      data: {
        label: 'レスポンシブデザイン',
        description: 'メディアクエリ、ビューポート、モバイルファースト',
        nodeId: 'responsive-design',
      },
      position: { x: 200, y: 320 },
    },
    {
      id: 'css-frameworks',
      type: 'optional',
      data: {
        label: 'CSSフレームワーク',
        description: 'Bootstrap、Tailwind CSS、Bulmaなど',
        nodeId: 'css-frameworks',
      },
      position: { x: 200, y: 390 },
    },
    {
      id: 'js-basics',
      type: 'secondary',
      data: {
        label: 'JavaScript基礎',
        description: '変数、データ型、関数、スコープ、イベント',
        nodeId: 'js-basics',
      },
      position: { x: 400, y: 180 },
    },
    {
      id: 'dom-manipulation',
      type: 'secondary',
      data: {
        label: 'DOM操作',
        description: '要素の選択、作成、更新、イベントリスナー',
        nodeId: 'dom-manipulation',
      },
      position: { x: 400, y: 250 },
    },
    {
      id: 'async-js',
      type: 'secondary',
      data: {
        label: '非同期JavaScript',
        description: 'コールバック、Promise、async/await',
        nodeId: 'async-js',
      },
      position: { x: 400, y: 320 },
    },
    {
      id: 'es6-plus',
      type: 'secondary',
      data: {
        label: 'ES6+の機能',
        description: 'アロー関数、分割代入、スプレッド構文、クラス',
        nodeId: 'es6-plus',
      },
      position: { x: 400, y: 390 },
    },
    {
      id: 'js-frameworks',
      type: 'secondary',
      position: { x: 125, y: 500 },
      data: {
        nodeId: 'js-frameworks',
        label: 'JavaScriptフレームワーク',
        description:
          'モダンなフロントエンド開発に使用される主要なJavaScriptフレームワーク（React、Vue、Angular）について学ぶ',
        color: '#ffeb3b',
      },
    },
    {
      id: 'react',
      type: 'optional',
      data: {
        label: 'React',
        description: 'コンポーネント、props、state、hooks、Reduxなど',
        nodeId: 'react',
      },
      position: { x: 400, y: 430 },
    },
    {
      id: 'vue',
      type: 'optional',
      data: {
        label: 'Vue.js',
        description: 'ディレクティブ、コンポーネント、Vuex、Composition API',
        nodeId: 'vue',
      },
      position: { x: 400, y: 500 },
    },
    {
      id: 'angular',
      type: 'optional',
      data: {
        label: 'Angular',
        description: 'コンポーネント、サービス、モジュール、RxJS',
        nodeId: 'angular',
      },
      position: { x: 400, y: 570 },
    },
    {
      id: 'web-performance',
      type: 'recommended',
      data: {
        label: 'Webパフォーマンス',
        description: 'パフォーマンス最適化、Core Web Vitals、バンドルサイズの削減について学ぶ',
        nodeId: 'web-performance',
      },
      position: { x: 150, y: 620 },
    },
    {
      id: 'performance-metrics',
      type: 'secondary',
      data: {
        label: 'パフォーマンス指標',
        description: 'LCP、FID、CLS、Webパフォーマンスの測定',
        nodeId: 'performance-metrics',
      },
      position: { x: 50, y: 700 },
    },
    {
      id: 'optimization',
      type: 'secondary',
      data: {
        label: '最適化テクニック',
        description: '画像最適化、遅延読み込み、コード分割、キャッシュ',
        nodeId: 'optimization',
      },
      position: { x: 250, y: 700 },
    },
  ];

  const edges: Edge[] = [
    {
      id: 'internet-to-how-internet-works',
      source: 'internet',
      target: 'how-internet-works',
      animated: true,
      sourceHandle: 'left',
      targetHandle: 'right',
    },
    {
      id: 'internet-to-http',
      source: 'internet',
      target: 'http',
      animated: true,
      sourceHandle: 'left',
      targetHandle: 'right',
    },

    {
      id: 'html-to-html-basics',
      source: 'html',
      target: 'html-basics',
      animated: true,
      sourceHandle: 'bottom',
      targetHandle: 'top',
    },
    {
      id: 'html-to-semantic-html',
      source: 'html',
      target: 'semantic-html',
      animated: true,
      sourceHandle: 'bottom',
      targetHandle: 'top',
    },
    {
      id: 'html-to-forms-validation',
      source: 'html',
      target: 'forms-validation',
      animated: true,
      sourceHandle: 'bottom',
      targetHandle: 'top',
    },
    {
      id: 'html-to-accessibility',
      source: 'html',
      target: 'accessibility',
      animated: true,
      sourceHandle: 'bottom',
      targetHandle: 'top',
    },

    {
      id: 'css-to-css-basics',
      source: 'css',
      target: 'css-basics',
      animated: true,
      sourceHandle: 'bottom',
      targetHandle: 'top',
    },
    {
      id: 'css-to-layout',
      source: 'css',
      target: 'layout',
      animated: true,
      sourceHandle: 'bottom',
      targetHandle: 'top',
    },
    {
      id: 'css-to-responsive-design',
      source: 'css',
      target: 'responsive-design',
      animated: true,
      sourceHandle: 'bottom',
      targetHandle: 'top',
    },
    {
      id: 'css-to-css-frameworks',
      source: 'css',
      target: 'css-frameworks',
      animated: true,
      sourceHandle: 'bottom',
      targetHandle: 'top',
    },

    {
      id: 'javascript-to-js-basics',
      source: 'javascript',
      target: 'js-basics',
      animated: true,
      sourceHandle: 'bottom',
      targetHandle: 'top',
    },
    {
      id: 'javascript-to-dom-manipulation',
      source: 'javascript',
      target: 'dom-manipulation',
      animated: true,
      sourceHandle: 'bottom',
      targetHandle: 'top',
    },
    {
      id: 'javascript-to-async-js',
      source: 'javascript',
      target: 'async-js',
      animated: true,
      sourceHandle: 'bottom',
      targetHandle: 'top',
    },
    {
      id: 'javascript-to-es6-plus',
      source: 'javascript',
      target: 'es6-plus',
      animated: true,
      sourceHandle: 'bottom',
      targetHandle: 'top',
    },

    {
      id: 'internet-to-html',
      source: 'internet',
      target: 'html',
      type: 'smoothstep',
      sourceHandle: 'bottom',
      targetHandle: 'top',
    },
    {
      id: 'internet-to-css',
      source: 'internet',
      target: 'css',
      type: 'smoothstep',
      sourceHandle: 'bottom',
      targetHandle: 'top',
    },
    {
      id: 'internet-to-javascript',
      source: 'internet',
      target: 'javascript',
      type: 'smoothstep',
      sourceHandle: 'bottom',
      targetHandle: 'top',
    },

    {
      id: 'html-to-js-frameworks',
      source: 'html',
      target: 'js-frameworks',
      type: 'smoothstep',
      sourceHandle: 'bottom',
      targetHandle: 'top',
    },
    {
      id: 'css-to-js-frameworks',
      source: 'css',
      target: 'js-frameworks',
      type: 'smoothstep',
      sourceHandle: 'bottom',
      targetHandle: 'top',
    },
    {
      id: 'javascript-to-js-frameworks',
      source: 'javascript',
      target: 'js-frameworks',
      type: 'smoothstep',
      sourceHandle: 'bottom',
      targetHandle: 'top',
    },

    {
      id: 'js-frameworks-to-react',
      source: 'js-frameworks',
      target: 'react',
      animated: true,
      style: { strokeDasharray: '5 5' },
      // type: 'smoothstep',
      sourceHandle: 'right',
      targetHandle: 'left',
    },
    {
      id: 'js-frameworks-to-vue',
      source: 'js-frameworks',
      target: 'vue',
      animated: true,
      style: { strokeDasharray: '5 5' },
      sourceHandle: 'right',
      targetHandle: 'left',
    },
    {
      id: 'js-frameworks-to-angular',
      source: 'js-frameworks',
      target: 'angular',
      animated: true,
      style: { strokeDasharray: '5 5' },
      // type: 'smoothstep',
      sourceHandle: 'right',
      targetHandle: 'left',
    },

    {
      id: 'js-frameworks-to-web-performance',
      source: 'js-frameworks',
      target: 'web-performance',
      type: 'smoothstep',
      sourceHandle: 'bottom',
    },

    {
      id: 'web-performance-to-performance-metrics',
      source: 'web-performance',
      target: 'performance-metrics',
      animated: true,
    },
    {
      id: 'web-performance-to-optimization',
      source: 'web-performance',
      target: 'optimization',
      animated: true,
    },
  ];

  return { nodes, edges };
};

// サンプルのロードマップデータ
const roadmaps: Record<string, Record<string, RoadmapData>> = {
  'web-development': {
    frontend: {
      id: 'frontend-development',
      title: 'フロントエンド開発ロードマップ',
      description:
        'フロントエンド開発の基本から応用までのロードマップです。HTML、CSS、JavaScriptなどの必須技術から、モダンなフレームワークまで学ぶことができます。',
      categoryId: 'web-development',
      categoryTitle: 'Web開発',
      themeId: 'frontend',
      themeTitle: 'フロントエンド開発',
      nodes: [
        {
          id: 'internet',
          title: 'インターネット',
          description:
            'インターネットの仕組み、ブラウザの動作原理、HTTP/HTTPSプロトコルについて学ぶ',
          type: 'primary',
          children: [],
          resources: [
            {
              title: 'インターネットの仕組み入門',
              url: 'https://developer.mozilla.org/ja/docs/Learn/Common_questions/How_does_the_Internet_work',
              type: 'article',
            },
            {
              title: 'HTTP完全ガイド - プロトコルの基礎から実践まで',
              url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
              type: 'video',
            },
            {
              title: 'ブラウザの仕組み：最新ウェブブラウザの内部構造',
              url: 'https://web.dev/articles/howbrowserswork?hl=ja',
              type: 'docs',
            },
            {
              title: 'ネットワークの基礎からわかるTCP/IP入門講座',
              url: 'https://www.udemy.com/course/tcp-ip-network/',
              type: 'course',
            },
            {
              title: 'HTTPの教科書',
              url: 'https://www.amazon.co.jp/dp/4774142042',
              type: 'book',
            },
          ],
        },
        // 他のノードは省略
      ],
    },
  },
};

export default function RoadmapPage() {
  const params = useParams();
  const router = useRouter();
  const categoryId = params?.category as string;
  const themeId = params?.theme as string;

  // React Flowのステート
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  // 全てのステートフックを先に定義
  const [roadmap, setRoadmap] = useState<RoadmapData | null>(null);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  // 全てのコールバックフックを定義
  const onNodeClick = useCallback((event: React.MouseEvent, node: Node) => {
    setSelectedNode(node.data.nodeId);
  }, []);

  const getNodeData = useCallback(
    (nodeId: string): RoadmapNode | null => {
      if (!roadmap) return null;

      const findNodeRecursive = (nodes: RoadmapNode[], id: string): RoadmapNode | null => {
        for (const node of nodes) {
          if (node.id === id) return node;
          if (node.children) {
            const found = findNodeRecursive(node.children, id);
            if (found) return found;
          }
        }
        return null;
      };

      return findNodeRecursive(roadmap.nodes, nodeId);
    },
    [roadmap]
  );

  // useEffectは最後に定義
  useEffect(() => {
    // カテゴリとテーマからロードマップデータを取得
    if (categoryId && themeId && roadmaps[categoryId]?.[themeId]) {
      setRoadmap(roadmaps[categoryId][themeId]);

      // フロントエンド開発のロードマップの場合、React Flow用のデータを設定
      if (categoryId === 'web-development' && themeId === 'frontend') {
        const { nodes: flowNodes, edges: flowEdges } = getFrontendNodesAndEdges();
        setNodes(flowNodes);
        setEdges(flowEdges);
        // 最初のノードを選択
        setSelectedNode('internet');
      } else {
        // 他のロードマップはまだ実装されていない
        if (categoryId) {
          router.push(`/roadmaps/${categoryId}`);
        } else {
          router.push('/roadmaps');
        }
      }
    } else {
      // 無効なカテゴリまたはテーマの場合はカテゴリページにリダイレクト
      if (categoryId) {
        router.push(`/roadmaps/${categoryId}`);
      } else {
        router.push('/roadmaps');
      }
    }
  }, [categoryId, themeId, router, setNodes, setEdges]);

  if (!roadmap) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-4">ロードマップを読み込み中...</p>
      </div>
    );
  }

  const selectedNodeData = selectedNode ? getNodeData(selectedNode) : null;

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8 flex flex-wrap items-center text-sm">
        <Link href="/roadmaps">
          <span className="text-blue-600 hover:underline">カテゴリ一覧</span>
        </Link>
        <span className="mx-2">&#8594;</span>
        <Link href={`/roadmaps/${categoryId}`}>
          <span className="text-blue-600 hover:underline">{roadmap.categoryTitle}</span>
        </Link>
        <span className="mx-2">&#8594;</span>
        <span className="font-medium">{roadmap.themeTitle}</span>
      </div>

      {/* ヘッダー情報とバージョン選択 */}
      <div className="flex flex-col md:flex-row justify-between items-start mb-4">
        <div>
          <h1 className="text-3xl font-bold mb-2">{roadmap.title}</h1>
          <p className="text-gray-600 mb-4">{roadmap.description}</p>
        </div>
        <div className="w-full md:w-64 mt-4 md:mt-0">
          <div className="mb-2 text-sm font-medium">ロードマップバージョン</div>
        </div>
      </div>

      <div className="flex flex-col md:flex-row gap-6">
        {/* ロードマップのフローチャート */}
        <div className="md:w-2/3 h-[700px] bg-gray-50 rounded-lg shadow-md">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onNodeClick={onNodeClick}
            nodeTypes={customNodeTypes}
            fitView
            attributionPosition="bottom-left"
          >
            <Controls />
            <MiniMap />
            <Background gap={12} size={1} />
            <Panel position="top-right">
              <div className="bg-white p-3 rounded-md shadow-md">
                <h3 className="font-medium text-sm mb-2">凡例:</h3>
                <div className="flex flex-col space-y-1 text-xs">
                  <div className="flex items-center">
                    <div className="w-4 h-4 mr-2" style={{ background: '#ffeb3b' }}></div>
                    <span>主要技術</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-4 h-4 mr-2" style={{ background: '#ffe082' }}></div>
                    <span>基本スキル</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-4 h-4 mr-2" style={{ background: '#c8e6c9' }}></div>
                    <span>推奨スキル</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-4 h-4 mr-2" style={{ background: '#ddd' }}></div>
                    <span>オプション</span>
                  </div>
                </div>
              </div>
            </Panel>
          </ReactFlow>
        </div>

        {/* 選択されたノードの詳細 */}
        <div className="md:w-1/3">
          {selectedNodeData ? (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold mb-4">{selectedNodeData.title}</h2>
              <p className="text-gray-600 mb-6">{selectedNodeData.description}</p>

              {selectedNodeData.resources && selectedNodeData.resources.length > 0 && (
                <>
                  <h3 className="text-xl font-semibold mb-3">学習リソース</h3>
                  <div className="space-y-4">
                    {selectedNodeData.resources.map((resource, idx) => (
                      <div key={idx} className="p-4 border rounded-lg hover:bg-gray-50">
                        <div className="flex items-center">
                          <div className="mr-3">
                            {resource.type === 'article' && (
                              <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                                記事
                              </span>
                            )}
                            {resource.type === 'video' && (
                              <span className="bg-red-100 text-red-800 text-xs px-2 py-1 rounded">
                                動画
                              </span>
                            )}
                            {resource.type === 'course' && (
                              <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                                コース
                              </span>
                            )}
                            {resource.type === 'book' && (
                              <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded">
                                書籍
                              </span>
                            )}
                            {resource.type === 'docs' && (
                              <span className="bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded">
                                ドキュメント
                              </span>
                            )}
                          </div>
                          <div>
                            <a
                              href={resource.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="font-medium hover:text-blue-600"
                            >
                              {resource.title}
                            </a>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </>
              )}

              <div className="mt-8 flex flex-wrap justify-center">
                <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors mr-4 mb-2">
                  完了としてマーク
                </button>
                <button className="px-4 py-2 border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition-colors mb-2">
                  スキップする
                </button>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-lg shadow-md p-6 text-center">
              <p className="text-gray-600">左側のロードマップからトピックを選択してください</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
