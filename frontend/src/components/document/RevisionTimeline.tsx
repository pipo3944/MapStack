import { DocumentRevisionResponse } from '@/api/model';
import Link from 'next/link';
import React from 'react';

interface RevisionTimelineProps {
  /**
   * ドキュメントID
   */
  documentId: string;
  /**
   * リビジョン（バージョン）のリスト
   */
  revisions: DocumentRevisionResponse[];
  /**
   * 現在選択されているバージョン
   */
  currentVersion?: string;
  /**
   * バージョンがクリックされた時のコールバック
   */
  onVersionClick?: (version: string) => void;
  /**
   * クラス名
   */
  className?: string;
}

/**
 * リビジョン履歴タイムラインコンポーネント
 *
 * ドキュメントのバージョン履歴をタイムライン形式で表示します
 */
export const RevisionTimeline: React.FC<RevisionTimelineProps> = ({
  documentId,
  revisions,
  currentVersion,
  onVersionClick,
  className = '',
}) => {
  // バージョンを新しい順に並べ替え
  const sortedRevisions = [...revisions].sort((a, b) => {
    return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
  });

  const handleVersionClick = (version: string) => {
    if (onVersionClick) {
      onVersionClick(version);
    }
  };

  return (
    <div className={`revision-timeline ${className}`}>
      <h3 className="text-lg font-semibold mb-4">バージョン履歴</h3>

      <div className="flow-root">
        <ul className="-mb-8">
          {sortedRevisions.map((revision, index) => (
            <li key={revision.version}>
              <div className="relative pb-8">
                {index !== sortedRevisions.length - 1 ? (
                  <span
                    className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                    aria-hidden="true"
                  />
                ) : null}
                <div className="relative flex space-x-3">
                  <div>
                    <span
                      className={`h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white
                        ${currentVersion === revision.version
                          ? 'bg-blue-500'
                          : 'bg-gray-400'}`}
                    >
                      <svg
                        className="h-5 w-5 text-white"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                      >
                        <path
                          fillRule="evenodd"
                          d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                          clipRule="evenodd"
                        />
                      </svg>
                    </span>
                  </div>
                  <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                    <div>
                      <button
                        onClick={() => handleVersionClick(revision.version)}
                        className={`text-sm font-medium ${
                          currentVersion === revision.version
                            ? 'text-blue-600'
                            : 'text-gray-900 hover:text-blue-600'
                        }`}
                      >
                        バージョン {revision.version}
                      </button>
                      <p className="text-sm text-gray-500">
                        {revision.change_summary || 'No change summary'}
                      </p>
                    </div>
                    <div className="text-right text-sm whitespace-nowrap text-gray-500">
                      <time dateTime={revision.created_at}>
                        {new Date(revision.created_at).toLocaleDateString()}
                      </time>
                    </div>
                  </div>
                </div>

                {index !== sortedRevisions.length - 1 && (
                  <div className="ml-12 mt-2 mb-4">
                    <Link
                      href={`/documents/${documentId}/diff?from=${sortedRevisions[index + 1].version}&to=${revision.version}`}
                      className="text-xs text-blue-600 hover:text-blue-800"
                    >
                      変更点を表示
                    </Link>
                  </div>
                )}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default RevisionTimeline;
