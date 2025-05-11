import { DocumentResponse } from '@/api/model';
import Link from 'next/link';
import React from 'react';

interface NodeDocumentLinksProps {
  /**
   * ノードに関連付けられたドキュメントのリスト
   */
  documents: DocumentResponse[];
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
 * ノードドキュメントリンクコンポーネント
 *
 * ノードに関連付けられたドキュメントのリンクを表示します
 */
export const NodeDocumentLinks: React.FC<NodeDocumentLinksProps> = ({
  documents,
  nodeId,
  className = '',
}) => {

  // ボタン部分を共通コンポーネントとして抽出
  const ActionButtons = () => (
    <div className="mt-4 flex flex-wrap gap-2">
      {/* 独立したドキュメント作成ボタン */}
      <Link
        href="/documents/new"
        className="inline-flex items-center px-3 py-1.5 border border-blue-600 text-xs font-medium rounded text-blue-600 bg-white hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        <svg
          className="-ml-0.5 mr-1.5 h-4 w-4"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fillRule="evenodd"
            d="M10 3a1 1 0 00-1 1v5H4a1 1 0 100 2h5v5a1 1 0 102 0v-5h5a1 1 0 100-2h-5V4a1 1 0 00-1-1z"
            clipRule="evenodd"
          />
        </svg>
        新規ドキュメント作成
      </Link>

      {/* 既存ドキュメントのリンクボタン */}
      <Link
        href={`/nodes/${nodeId}/link-document`}
        className="inline-flex items-center px-3 py-1.5 border border-gray-300 text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        <svg
          className="-ml-0.5 mr-1.5 h-4 w-4"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fillRule="evenodd"
            d="M7.707 3.293a1 1 0 010 1.414L5.414 7H11a7 7 0 017 7v2a1 1 0 11-2 0v-2a5 5 0 00-5-5H5.414l2.293 2.293a1 1 0 11-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
            clipRule="evenodd"
          />
        </svg>
        既存ドキュメントをリンク
      </Link>
    </div>
  );

  if (documents.length === 0) {
    return (
      <div className={`node-document-links ${className}`}>
        <p className="text-gray-500 italic">関連ドキュメントはありません</p>

        <ActionButtons />
      </div>
    );
  }

  return (
    <div className={`node-document-links ${className}`}>
      <h3 className="text-lg font-semibold mb-3">関連ドキュメント</h3>

      <ul className="divide-y divide-gray-200">
        {documents.map((document) => (
          <li key={document.id} className="py-3">
            <Link
              href={`/documents/${document.id}`}
              className="block hover:bg-gray-50 p-2 rounded transition-colors"
            >
              <div className="flex items-start">
                <div className="flex-shrink-0">
                  <svg
                    className="h-5 w-5 text-gray-400"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
                <div className="ml-3 flex-1">
                  <p className="text-sm font-medium text-blue-600">{document.title}</p>
                  {document.description && (
                    <p className="text-sm text-gray-500 line-clamp-2">{document.description}</p>
                  )}
                  <p className="mt-1 text-xs text-gray-400">
                    作成日: {new Date(document.created_at).toLocaleDateString()}
                    {document.updated_at && document.updated_at !== document.created_at && (
                      <> | 更新日: {new Date(document.updated_at).toLocaleDateString()}</>
                    )}
                  </p>
                </div>
              </div>
            </Link>
          </li>
        ))}
      </ul>

      <ActionButtons />
    </div>
  );
};

export default NodeDocumentLinks;
