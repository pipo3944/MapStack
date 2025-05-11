import { DocumentRevisionResponse } from '@/api/model';
import React from 'react';

interface VersionSelectorProps {
  /**
   * 利用可能なバージョンのリスト
   */
  versions: DocumentRevisionResponse[];
  /**
   * 現在選択されているバージョン
   */
  currentVersion: string;
  /**
   * バージョンが変更された時のコールバック
   */
  onVersionChange: (version: string) => void;
  /**
   * クラス名
   */
  className?: string;
}

/**
 * バージョン選択コンポーネント
 *
 * ドキュメントのバージョンをドロップダウンで選択できるようにします
 */
export const VersionSelector: React.FC<VersionSelectorProps> = ({
  versions,
  currentVersion,
  onVersionChange,
  className = '',
}) => {
  // バージョンを新しい順に並べ替え
  const sortedVersions = [...versions].sort((a, b) => {
    return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
  });

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onVersionChange(e.target.value);
  };

  return (
    <div className={`version-selector flex items-center ${className}`}>
      <span className="mr-2 text-sm font-medium text-gray-700">バージョン:</span>
      <select
        value={currentVersion}
        onChange={handleChange}
        className="form-select block w-auto py-1.5 px-3 text-base font-normal text-gray-700
                 bg-white bg-clip-padding bg-no-repeat border border-solid border-gray-300
                 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white
                 focus:border-blue-600 focus:outline-none"
      >
        {sortedVersions.map((version) => (
          <option key={version.version} value={version.version}>
            {version.version} ({new Date(version.created_at).toLocaleString()})
            {version.change_summary ? ` - ${version.change_summary}` : ''}
          </option>
        ))}
      </select>
    </div>
  );
};

export default VersionSelector;
