import { NodeDocumentLinks } from '@/components/document';
import { useNodeDocuments } from '@/hooks';
import React from 'react';

interface NodeDocumentSectionProps {
  /**
   * ノードID
   */
  nodeId: string;
  /**
   * クラス名
   */
  className?: string;
}

/**
 * ノードドキュメントセクションコンポーネント
 *
 * ロードマップノードに関連付けられたドキュメントを表示するセクション
 */
export const NodeDocumentSection: React.FC<NodeDocumentSectionProps> = ({
  nodeId,
  className = '',
}) => {
  // APIフックを使用してデータを取得
  const { getNodeDocuments } = useNodeDocuments();
  const nodeDocumentsQuery = getNodeDocuments(nodeId);

  // ローディング表示
  if (nodeDocumentsQuery.isLoading) {
    return (
      <div className={`node-document-section ${className}`}>
        <h3 className="text-lg font-semibold mb-3">関連ドキュメント</h3>
        <div className="flex justify-center py-4">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
        </div>
      </div>
    );
  }

  // エラー表示
  if (nodeDocumentsQuery.isError) {
    return (
      <div className={`node-document-section ${className}`}>
        <h3 className="text-lg font-semibold mb-3">関連ドキュメント</h3>
        <div className="p-4 bg-red-50 text-red-700 rounded-md">
          <p>ドキュメント情報の取得に失敗しました</p>
        </div>
      </div>
    );
  }

  // データがない場合
  if (!nodeDocumentsQuery.data) {
    return (
      <div className={`node-document-section ${className}`}>
        <h3 className="text-lg font-semibold mb-3">関連ドキュメント</h3>
        <p className="text-gray-500 italic">データがありません</p>
      </div>
    );
  }

  const documents = nodeDocumentsQuery.data.documents || [];

  return (
    <div className={`node-document-section ${className}`}>
      <NodeDocumentLinks
        documents={documents}
        nodeId={nodeId}
      />
    </div>
  );
};

export default NodeDocumentSection;
