import { DocumentContentBase } from '@/api/model';
import React from 'react';

interface DocumentViewerProps {
  /**
   * 表示するドキュメントのコンテンツ
   */
  document: DocumentContentBase;
  /**
   * 読み取り専用モードかどうか
   */
  readOnly?: boolean;
  /**
   * クラス名
   */
  className?: string;
}

/**
 * ドキュメントビューアーコンポーネント
 *
 * ドキュメントのタイトルとセクションを表示します
 */
export const DocumentViewer: React.FC<DocumentViewerProps> = ({
  document,
  readOnly = true,
  className = '',
}) => {
  return (
    <div className={`document-viewer ${className}`}>
      <h1 className="text-2xl font-bold mb-6">{document.title}</h1>

      <div className="document-sections space-y-6">
        {document.sections.map((section, index) => (
          <section key={index} className="document-section">
            <h2 className="text-xl font-semibold mb-2">{section.title}</h2>
            <div className="prose max-w-none">
              {section.content.split('\n').map((paragraph, pIndex) => (
                <p key={pIndex} className="mb-4">
                  {paragraph}
                </p>
              ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  );
};

export default DocumentViewer;
