import { DocumentRevisionDiff, DocumentSectionBase } from '@/api/model';
import React from 'react';

// 型定義の拡張
interface ModifiedSection {
  old_section: DocumentSectionBase;
  new_section: DocumentSectionBase;
}

interface DiffViewerProps {
  /**
   * 表示する差分データ
   */
  diff: DocumentRevisionDiff;
  /**
   * クラス名
   */
  className?: string;
}

/**
 * 差分表示コンポーネント
 *
 * ドキュメントの2つのバージョン間の差分を表示します
 */
export const DiffViewer: React.FC<DiffViewerProps> = ({
  diff,
  className = '',
}) => {
  const { from_version, to_version, sections_added = [], sections_removed = [], sections_modified = [] } = diff;

  // セクションの内容を表示する関数
  const renderSection = (section: DocumentSectionBase, type: 'added' | 'removed' | 'unchanged') => {
    const bgColor = type === 'added'
      ? 'bg-green-50 border-green-200'
      : type === 'removed'
        ? 'bg-red-50 border-red-200'
        : '';

    return (
      <div className={`p-4 mb-4 border rounded-md ${bgColor}`}>
        <h3 className="text-lg font-medium mb-2">{section.title}</h3>
        <div className="prose max-w-none">
          {section.content.split('\n').map((paragraph, pIndex) => (
            <p key={pIndex} className="mb-2">
              {paragraph}
            </p>
          ))}
        </div>
      </div>
    );
  };

  // 変更されたセクションの差分を表示する関数
  const renderModifiedSection = (index: number) => {
    // 型アサーションを使用して正しい型に変換
    const modifiedSection = sections_modified[index] as unknown as ModifiedSection;

    return (
      <div className="p-4 mb-4 border border-yellow-200 rounded-md bg-yellow-50">
        <h3 className="text-lg font-medium mb-2">
          {modifiedSection.old_section.title}
          {modifiedSection.old_section.title !== modifiedSection.new_section.title && (
            <span className="text-yellow-600"> → {modifiedSection.new_section.title}</span>
          )}
        </h3>

        <div className="grid grid-cols-2 gap-4">
          <div className="old-content">
            <h4 className="text-sm font-medium text-gray-500 mb-2">旧バージョン</h4>
            <div className="prose max-w-none text-red-800">
              {modifiedSection.old_section.content.split('\n').map((paragraph, pIndex) => (
                <p key={pIndex} className="mb-2">
                  {paragraph}
                </p>
              ))}
            </div>
          </div>

          <div className="new-content">
            <h4 className="text-sm font-medium text-gray-500 mb-2">新バージョン</h4>
            <div className="prose max-w-none text-green-800">
              {modifiedSection.new_section.content.split('\n').map((paragraph, pIndex) => (
                <p key={pIndex} className="mb-2">
                  {paragraph}
                </p>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className={`diff-viewer ${className}`}>
      <div className="mb-6">
        <h2 className="text-xl font-bold mb-2">バージョン比較</h2>
        <p className="text-gray-600">
          {from_version} から {to_version} への変更点
        </p>
      </div>

      {sections_added.length > 0 && (
        <div className="mb-8">
          <h3 className="text-lg font-semibold mb-3 text-green-700">追加されたセクション</h3>
          {sections_added.map((section, index) => (
            <div key={`added-${index}`}>
              {renderSection(section, 'added')}
            </div>
          ))}
        </div>
      )}

      {sections_removed.length > 0 && (
        <div className="mb-8">
          <h3 className="text-lg font-semibold mb-3 text-red-700">削除されたセクション</h3>
          {sections_removed.map((section, index) => (
            <div key={`removed-${index}`}>
              {renderSection(section, 'removed')}
            </div>
          ))}
        </div>
      )}

      {sections_modified.length > 0 && (
        <div className="mb-8">
          <h3 className="text-lg font-semibold mb-3 text-yellow-700">変更されたセクション</h3>
          {sections_modified.map((_, index) => (
            <div key={`modified-${index}`}>
              {renderModifiedSection(index)}
            </div>
          ))}
        </div>
      )}

      {sections_added.length === 0 && sections_removed.length === 0 && sections_modified.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          <p>変更はありません</p>
        </div>
      )}
    </div>
  );
};

export default DiffViewer;
