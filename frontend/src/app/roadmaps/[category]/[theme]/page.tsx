'use client';

import {
  useReadCategoryApiV1CategoriesCategoryIdGet,
  useReadRoadmapEdgesApiV1RoadmapsRoadmapIdEdgesGet,
  useReadRoadmapNodesApiV1RoadmapsRoadmapIdNodesGet,
  useReadRoadmapVersionsApiV1ThemesThemeIdRoadmapsVersionsGet,
  useReadThemeApiV1ThemesThemeIdGet,
} from '@/api/generated/roadmap/roadmap';
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

// リソースの型定義
interface Resource {
  title: string;
  url: string;
  type: 'article' | 'video' | 'course' | 'book' | 'docs';
}

// ノードデータの型定義
interface NodeData {
  label: string;
  description: string;
  nodeId: string;
  resources?: Resource[];
}

// RoadmapVersionの型定義
interface RoadmapVersion {
  id: string;
  version: string;
  title: string;
  is_published: boolean;
  is_latest: boolean;
  published_at: string | null;
  created_at: string;
}

// APIデータの型定義
interface RoadmapNodeData {
  id: string;
  roadmap_id: string;
  handle: string;
  node_type: string;
  title: string;
  description: string;
  position_x: number;
  position_y: number;
  meta_data: {
    resources?: Resource[];
    [key: string]: unknown;
  };
  is_required: boolean;
  created_at: string;
  updated_at: string;
}

interface RoadmapEdgeData {
  id: string;
  roadmap_id: string;
  handle: string;
  source_node_id: string;
  target_node_id: string;
  edge_type: string;
  source_handle: string | null;
  target_handle: string | null;
  meta_data: {
    style?: Record<string, unknown>;
    animated?: boolean;
    [key: string]: unknown;
  };
  label?: string;
  created_at: string;
  updated_at: string;
}

// カスタムノードタイプを統合
const customNodeTypes: NodeTypes = {
  ...nodeTypes,
};

// APIデータをReactFlowのノードとエッジに変換する関数
const convertApiDataToReactFlow = (apiNodes: RoadmapNodeData[], apiEdges: RoadmapEdgeData[]) => {
  // APIから取得したノードデータをReactFlow用に変換
  const nodes: Node[] = apiNodes.map((node) => ({
    id: node.id,
    type: node.node_type || 'primary', // ノードタイプがない場合はデフォルト
    position: { x: node.position_x || 0, y: node.position_y || 0 },
    data: {
      label: node.title,
      description: node.description || '',
      nodeId: node.handle,
      // メタデータに学習リソースがあれば変換
      resources: node.meta_data?.resources || [],
    },
  }));

  // APIから取得したエッジデータをReactFlow用に変換
  const edges: Edge[] = apiEdges.map((edge) => ({
    id: edge.id,
    source: edge.source_node_id,
    target: edge.target_node_id,
    // エッジタイプが指定されていればそれを使用
    type: edge.edge_type === 'default' ? 'smoothstep' : edge.edge_type,
    // メタデータからスタイル情報を取得
    style: edge.meta_data?.style || {},
    // アニメーション設定など
    animated: edge.meta_data?.animated || false,
    // ハンドル情報
    sourceHandle: edge.source_handle || null,
    targetHandle: edge.target_handle || null,
    // ラベルがあれば追加
    label: edge.label || '',
  }));

  return { nodes, edges };
};

// フロントエンドのサンプルデータ（APIからデータが取得できない場合のフォールバック用）
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

export default function RoadmapPage() {
  const params = useParams();
  const router = useRouter();
  const categoryId = params?.category as string;
  const themeId = params?.theme as string;

  // React Flowのステート
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  // 選択中のロードマップIDとバージョン
  const [selectedRoadmapId, setSelectedRoadmapId] = useState<string | null>(null);
  const [roadmapVersions, setRoadmapVersions] = useState<RoadmapVersion[]>([]);
  const [isUsingDemoData, setIsUsingDemoData] = useState(false);

  // APIからカテゴリ情報を取得
  const {
    data: categoryData,
    isLoading: isLoadingCategory,
    error: categoryError,
  } = useReadCategoryApiV1CategoriesCategoryIdGet(categoryId);

  // APIからテーマ情報を取得
  const {
    data: themeData,
    isLoading: isLoadingTheme,
    error: themeError,
  } = useReadThemeApiV1ThemesThemeIdGet(themeId);

  // APIからテーマに関連するロードマップバージョン一覧を取得
  const {
    data: versionsData,
    isLoading: isLoadingVersions,
    error: versionsError,
  } = useReadRoadmapVersionsApiV1ThemesThemeIdRoadmapsVersionsGet(themeId);

  // 選択したロードマップのノードを取得
  const {
    data: nodesData,
    isLoading: isLoadingNodes,
    error: nodesError,
  } = useReadRoadmapNodesApiV1RoadmapsRoadmapIdNodesGet(selectedRoadmapId || '', {
    query: { enabled: !!selectedRoadmapId },
  });

  // 選択したロードマップのエッジを取得
  const {
    data: edgesData,
    isLoading: isLoadingEdges,
    error: edgesError,
  } = useReadRoadmapEdgesApiV1RoadmapsRoadmapIdEdgesGet(selectedRoadmapId || '', {
    query: { enabled: !!selectedRoadmapId },
  });

  // ロードマップ情報のステート
  const [roadmapInfo, setRoadmapInfo] = useState({
    title: '',
    description: '',
    categoryTitle: '',
    themeTitle: '',
    version: '',
  });

  // 選択されたノード情報のステート
  const [selectedNodeData, setSelectedNodeData] = useState<NodeData | null>(null);

  // カテゴリーとテーマのデータが取得できたらロードマップ情報を更新
  useEffect(() => {
    if (categoryData?.success && categoryData.data && themeData?.success && themeData.data) {
      setRoadmapInfo({
        title: `${themeData.data.title}ロードマップ`,
        description: themeData.data.description || '',
        categoryTitle: categoryData.data.title,
        themeTitle: themeData.data.title,
        version: '',
      });
    }
  }, [categoryData, themeData]);

  // ロードマップバージョンデータが取得できたら処理
  useEffect(() => {
    if (versionsData?.success && versionsData.data && versionsData.data.length > 0) {
      setRoadmapVersions(versionsData.data);

      // 最新の公開済みバージョンを探す
      const publishedVersions = versionsData.data.filter((v: RoadmapVersion) => v.is_published);
      const latestVersion =
        publishedVersions.length > 0 ? publishedVersions[0] : versionsData.data[0];

      // 最新バージョンのロードマップIDを設定
      setSelectedRoadmapId(latestVersion.id);

      // バージョン情報を更新
      setRoadmapInfo((prev) => ({
        ...prev,
        version: latestVersion.version,
      }));
    }
  }, [versionsData]);

  // ノードとエッジのデータが取得できたら処理
  useEffect(() => {
    if (selectedRoadmapId && nodesData && edgesData) {
      // APIから取得したデータがある場合
      if (nodesData.length > 0 || edgesData.length > 0) {
        // APIのレスポンスデータを適切な型に変換
        const apiNodes = nodesData as unknown as RoadmapNodeData[];
        const apiEdges = edgesData as unknown as RoadmapEdgeData[];

        const { nodes: flowNodes, edges: flowEdges } = convertApiDataToReactFlow(
          apiNodes,
          apiEdges
        );
        setNodes(flowNodes);
        setEdges(flowEdges);

        // 最初のノードを選択
        if (flowNodes.length > 0) {
          setSelectedNodeData(flowNodes[0].data as NodeData);
        }

        setIsUsingDemoData(false);
      } else {
        // APIからデータが取得できない場合はデモデータを使用
        const { nodes: flowNodes, edges: flowEdges } = getFrontendNodesAndEdges();
        setNodes(flowNodes);
        setEdges(flowEdges);

        // 最初のノードを選択
        setSelectedNodeData(flowNodes[0].data as NodeData);

        setIsUsingDemoData(true);
      }
    }
  }, [selectedRoadmapId, nodesData, edgesData, setNodes, setEdges]);

  // ロードマップバージョン選択時の処理
  const handleVersionChange = (versionId: string) => {
    setSelectedRoadmapId(versionId);

    // 選択したバージョンの情報を設定
    const selectedVersion = roadmapVersions.find((v) => v.id === versionId);
    if (selectedVersion) {
      setRoadmapInfo((prev) => ({
        ...prev,
        version: selectedVersion.version,
      }));
    }
  };

  // ノードクリック時の処理
  const onNodeClick = useCallback((event: React.MouseEvent, node: Node) => {
    setSelectedNodeData(node.data as NodeData);
  }, []);

  // 初期化処理
  useEffect(() => {
    // APIからデータを取得する前に最初に呼び出されるため
    // カテゴリIDとテーマIDのバリデーションのみ行う
    if (!categoryId || !themeId) {
      if (categoryId) {
        router.push(`/roadmaps/${categoryId}`);
      } else {
        router.push('/roadmaps');
      }
    }
  }, [categoryId, themeId, router]);

  // ローディング中の表示
  if (
    isLoadingCategory ||
    isLoadingTheme ||
    isLoadingVersions ||
    (selectedRoadmapId && (isLoadingNodes || isLoadingEdges))
  ) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-4">ロードマップを読み込み中...</p>
      </div>
    );
  }

  // エラー時の表示
  if (
    categoryError ||
    themeError ||
    versionsError ||
    (selectedRoadmapId && (nodesError || edgesError)) ||
    !categoryData?.success ||
    !themeData?.success
  ) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <h1 className="text-3xl font-bold mb-8 text-red-500">エラーが発生しました</h1>
        <p className="text-gray-600 mb-4">
          データの取得中に問題が発生しました。後でもう一度お試しください。
        </p>
        <div className="flex justify-center gap-4">
          <button
            onClick={() => window.location.reload()}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            再読み込み
          </button>
          <Link href={`/roadmaps/${categoryId}`}>
            <span className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded inline-block">
              カテゴリ詳細に戻る
            </span>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8 flex flex-wrap items-center text-sm">
        <Link href="/roadmaps">
          <span className="text-blue-600 hover:underline">カテゴリ一覧</span>
        </Link>
        <span className="mx-2">&#8594;</span>
        <Link href={`/roadmaps/${categoryId}`}>
          <span className="text-blue-600 hover:underline">{roadmapInfo.categoryTitle}</span>
        </Link>
        <span className="mx-2">&#8594;</span>
        <span className="font-medium">{roadmapInfo.themeTitle}</span>
      </div>

      {/* ヘッダー情報とバージョン選択 */}
      <div className="flex flex-col md:flex-row justify-between items-start mb-4">
        <div>
          <h1 className="text-3xl font-bold mb-2">{roadmapInfo.title}</h1>
          <p className="text-gray-600 mb-4">{roadmapInfo.description}</p>
        </div>
        <div className="w-full md:w-64 mt-4 md:mt-0">
          <div className="mb-2 text-sm font-medium">ロードマップバージョン</div>
          {roadmapVersions.length > 0 ? (
            <select
              className="w-full p-2 border rounded"
              value={selectedRoadmapId || ''}
              onChange={(e) => handleVersionChange(e.target.value)}
            >
              {roadmapVersions.map((version: RoadmapVersion) => (
                <option key={version.id} value={version.id}>
                  {version.version} {version.is_latest ? '(最新)' : ''}{' '}
                  {version.is_published ? '(公開済)' : '(非公開)'}
                </option>
              ))}
            </select>
          ) : (
            <div className="p-2 bg-gray-100 rounded text-sm">
              {isUsingDemoData
                ? 'バージョンがありません。デモデータを表示しています。'
                : 'バージョン情報を取得中...'}
            </div>
          )}
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
              <h2 className="text-2xl font-bold mb-4">{selectedNodeData.label}</h2>
              <p className="text-gray-600 mb-6">{selectedNodeData.description}</p>

              {selectedNodeData.resources && selectedNodeData.resources.length > 0 && (
                <>
                  <h3 className="text-xl font-semibold mb-3">学習リソース</h3>
                  <div className="space-y-4">
                    {selectedNodeData.resources.map((resource: Resource, idx: number) => (
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
